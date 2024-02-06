// eslint-disable-next-line no-unused-vars
/* global updateNewChatButtonNotSynced, getAllConversations, getConversation, loadConversationList, initializeTimestamp, isGenerating, prependConversation, addToTheTopOfConversationList, generateTitleForConversation, canSubmitPrompt, formatDate, userChatIsActuallySaved:true, addAsyncInputEvents, addSyncBanner, isWindows, sortConversationsByTimestamp, renderGPTList, getConversations, formatTime */
/* eslint-disable no-await-in-loop, */
let autoSaveTimeoutId;

// eslint-disable-next-line no-unused-vars
async function autoSaveCountDownAsync() {
  await new Promise((resolve) => {
    autoSaveTimeoutId = setTimeout(() => {
      resolve();
    }, 200);
  });
}
async function addConversationToStorage(localConversations, remoteConvId) {
  const newLocalConversations = await getConversation(remoteConvId).then((conversation) => {
    if (!conversation) {
      delete localConversations[remoteConvId];
      return localConversations;
    }
    Object.keys(conversation.mapping).forEach((key) => {
      if (localConversations[remoteConvId] && localConversations[remoteConvId]?.mapping[key] && localConversations[remoteConvId]?.mapping[key]?.pinned) {
        conversation.mapping[key].pinned = true;
      }
    });
    localConversations[remoteConvId] = {
      ...conversation,
      id: remoteConvId,
      saveHistory: true,
      shouldRefresh: false,
      update_time: formatTime(conversation.update_time),
    };
    chrome.storage.local.set({
      conversations: localConversations,
    });
    return localConversations;
  }, () => localConversations);
  return newLocalConversations;
}
// eslint-disable-next-line no-unused-vars
function updateOutOfDateConversation() {
  chrome.storage.local.get(['conversations'], (result) => {
    const { conversations } = result;
    if (!conversations) return;
    const outOfDateConversations = Object.values(conversations).filter((conv) => conv?.saveHistory !== false && (conv.shouldRefresh || conv.update_time === 'force_copy'));
    if (outOfDateConversations.length === 0) return;
    outOfDateConversations.forEach((conv) => {
      updateConversationInStorage(conversations, conv.id, true);
    });
  });
}
async function updateConversationInStorage(localConversations, localConvId, forceRefresh = false) {
  const newLocalConversations = await getConversation(localConvId, forceRefresh).then((conversation) => {
    if (!conversation || !conversation?.conversation_id) {
      delete localConversations[localConvId];
      return localConversations;
    }
    Object.keys(conversation.mapping)?.forEach((key) => {
      if (localConversations[localConvId] && localConversations[localConvId]?.mapping?.[key] && localConversations[localConvId]?.mapping?.[key]?.pinned) {
        conversation.mapping[key].pinned = true;
      }
    });
    localConversations[localConvId] = {
      ...localConversations[localConvId],
      ...conversation,
      update_time: formatTime(conversation.update_time),
      shouldRefresh: false,
    };
    chrome.storage.local.set({
      conversations: localConversations,
    });
    return localConversations;
  }, () => localConversations);
  return newLocalConversations;
}
// eslint-disable-next-line no-unused-vars
function unarchiveConversationById(conversationId, fullUnarchive = true) {
  return chrome.storage.local.get(['conversations']).then(async (result) => {
    const { conversations } = result;
    const newConversations = await addConversationToStorage(conversations, conversationId);
    if (fullUnarchive) { // add to the top of the list and conversationsOrder
      addToTheTopOfConversationList(newConversations[conversationId]); // this will take care of updating the conversationsOrder too
    }
    if (Object.keys(newConversations).includes(conversationId)) {
      return true;
    }
    return false;
  });
}
// eslint-disable-next-line no-unused-vars
function updateOrCreateConversation(conversationId, gizmoId, messages, parentId, settings, generateTitle = false, forceRefresh = false, newSystemMessage = {}) {
  if (!messages || messages.length === 0) return;
  // eslint-disable-next-line consistent-return
  return chrome.storage.local.get(['conversations', 'enabledPluginIds', 'selectedModel']).then((result) => {
    const existingConversation = result.conversations?.[conversationId];
    if (existingConversation) {
      existingConversation.languageCode = settings.selectedLanguage.code;
      existingConversation.toneCode = settings.selectedTone.code;
      existingConversation.writingStyleCode = settings.selectedWritingStyle.code;
      existingConversation.shouldRefresh = forceRefresh;
      existingConversation.current_node = messages[messages.length - 1].id;
      existingConversation.update_time = 'force_copy';
      messages.forEach((message, index) => {
        if (!message.create_time) message.create_time = (new Date()).getTime();
        const pid = index === 0 ? parentId : messages[index - 1]?.id;
        if (existingConversation.mapping[message.id]?.id) {
          existingConversation.mapping[message.id].message = message;
        } else {
          existingConversation.mapping[message.id] = {
            children: [], id: message.id, message, parent: pid,
          };
        }
        if (pid) {
          // eslint-disable-next-line prefer-destructuring
          const children = existingConversation.mapping[pid]?.children;
          if (children && !children.includes(message.id)) {
            existingConversation.mapping[pid].children.push(message.id);
          }
        }
      });
      return chrome.storage.local.set(
        {
          conversations: {
            ...result.conversations,
            [conversationId]: existingConversation,
          },
        },
      ).then(
        () => {
          userChatIsActuallySaved = true;
          const mapping = Object.values(existingConversation.mapping);
          const userMessages = mapping.filter((m) => (m.message?.role === 'user' || m.message?.author?.role === 'user') && m.message.recipient === 'all');
          const assistantMessages = mapping.filter((m) => (m.message?.role === 'assistant' || m.message?.author?.role === 'assistant') && m.message.recipient === 'all');
          if (generateTitle && existingConversation.title === 'New chat' && userMessages.length === 1 && assistantMessages.length > 0) { // only one assistant message
            if (settings.saveHistory) {
              // find last system message
              const allSystemMessages = mapping.filter((m) => m.message?.role === 'system' || m.message?.author?.role === 'system');

              const systemMessageWithCustomInstruction = allSystemMessages.find((node) => node?.message?.metadata?.user_context_message_data);
              const customInstrucionProfile = systemMessageWithCustomInstruction?.message?.metadata?.user_context_message_data || undefined;
              generateTitleForConversation(existingConversation.id, messages[messages.length - 1].id, customInstrucionProfile);
            }
          } else { // === updated
            // move cnversationelemnt to the top of the list
            const conversationElement = document.querySelector(`#conversation-button-${conversationId}`);
            const conversationUpdateTime = formatDate(new Date());
            const searchBoxWrapper = document.querySelector('#conversation-search-wrapper');

            if (conversationElement && searchBoxWrapper) {
              const conversationTimestampElement = conversationElement.querySelector('#timestamp');
              conversationTimestampElement.innerHTML = conversationUpdateTime;
              let lastFolderAtTheTop = searchBoxWrapper;
              while (lastFolderAtTheTop.nextElementSibling.id.startsWith('wrapper-folder-')) {
                lastFolderAtTheTop = lastFolderAtTheTop.nextElementSibling;
              }
              // update conversationsOrder
              chrome.storage.local.get(['conversationsOrder'], (res) => {
                const { conversationsOrder } = res;
                const conversationIndex = conversationsOrder.findIndex((conv) => conv === conversationId);
                if (conversationIndex === -1) {
                  // find folder containing conversation
                  const folderContainingConversation = conversationsOrder.find((conv) => typeof conv === 'object' && conv?.conversationIds.includes(conversationId));
                  if (folderContainingConversation) {
                    const folderContentElement = document.querySelector(`#folder-content-${folderContainingConversation.id}`);
                    if (folderContentElement) {
                      folderContentElement.prepend(conversationElement);
                      folderContainingConversation.conversationIds.splice(folderContainingConversation.conversationIds.indexOf(conversationId), 1);
                      folderContainingConversation.conversationIds.unshift(conversationId);
                      chrome.storage.local.set({
                        conversationsOrder,
                      });
                    }
                  }
                } else {
                  // this guarantees we only move if conversation is not in a folder
                  lastFolderAtTheTop.after(conversationElement);
                  // find the folder with id matching the wrapper-folder id
                  const lastFolderAtTheTopIndex = conversationsOrder.findIndex((conv) => conv?.id === lastFolderAtTheTop.id.split('wrapper-folder-')[1]);
                  conversationsOrder.splice(conversationIndex, 1);
                  conversationsOrder.splice(lastFolderAtTheTopIndex, 0, conversationId);

                  chrome.storage.local.set({
                    conversationsOrder,
                  });
                }
                conversationElement.scrollIntoView({ block: 'center' });
              });
            }
          }
        },
      );
    }
    const systemMessage = {
      id: newSystemMessage.id,
      message: { ...newSystemMessage },
      parent: parentId,
      children: [
        messages[0].id,
      ],
    };
    const newConversation = {
      id: conversationId,
      shouldRefresh: false,
      saveHistory: settings.saveHistory,
      languageCode: settings.selectedLanguage?.code,
      toneCode: settings.selectedTone?.code,
      writingStyleCode: settings.selectedWritingStyle?.code,
      current_node: messages[0].id,
      title: 'New chat',
      create_time: (new Date()).getTime(),
      update_time: 'force_copy',
      mapping: {
        [parentId]: {
          children: [systemMessage.id], id: parentId, message: null, parent: null,
        },
        [systemMessage.id]: systemMessage,
        [messages[0].id]: {
          children: [], id: messages[0].id, message: messages[0], parent: systemMessage.id,
        },
      },
      moderation_results: [],
    };
    if (result.selectedModel.slug.includes('plugins')) {
      newConversation.pluginIds = result.enabledPluginIds;
    }
    if (gizmoId) {
      newConversation.gizmo_id = gizmoId;
      newConversation.conversation_template_id = gizmoId;
    }
    return chrome.storage.local.set({
      conversations: {
        ...result.conversations,
        [conversationId]: newConversation,
      },
    }).then(() => {
      userChatIsActuallySaved = true;
      prependConversation(newConversation, settings);
      if (gizmoId) {
        setTimeout(() => {
          const showMoreButton = document.querySelector('#show-more-button');
          renderGPTList(showMoreButton?.innerText?.includes('less'), true);
        }, 1500);
      }
    });
  });
}
function addProgressBar() {
  const existingSyncDiv = document.getElementById('sync-div');
  if (existingSyncDiv) existingSyncDiv.remove();

  const nav = document.querySelector('nav');
  if (!nav) return;
  nav.style.position = 'relative';
  nav.style.overflow = 'hidden';
  const progressBar = document.createElement('div');
  progressBar.classList = 'absolute bottom-0 left-0 z-50 animate-pulse text-token-text-secondary';
  progressBar.style = 'height:1px;width: 100%; background-color: #00aaff;margin:0;';
  progressBar.id = 'sync-progressbar';
  const progressLabel = document.createElement('div');
  progressLabel.classList = 'absolute bottom-1 right-1 z-50 text-xs text-token-text-secondary';
  progressLabel.id = 'sync-progresslabel';
  progressLabel.innerText = 'Syncing...';

  const tooltip = document.createElement('div');
  tooltip.classList = 'flex z-50 text-xs rounded p-2';
  tooltip.style = 'position: absolute; width: 250px; border: solid 1px #8e8ea0; bottom: 20px; right: 4px; background-color: #343541; display:none; margin:0;';
  tooltip.id = 'sync-tooltip';
  tooltip.innerText = 'You conversations are being backed up in your computer for a faster experience! This can take a while.';
  progressLabel.addEventListener('mouseover', () => {
    tooltip.style.display = 'block';
  });
  progressLabel.addEventListener('mouseout', () => {
    tooltip.style.display = 'none';
  });
  const refreshButton = document.createElement('div');
  refreshButton.id = 'sync-refresh-button';
  refreshButton.classList = 'z-50 text-xs text-token-text-secondary w-3 h-3 m-0';
  refreshButton.style = 'position: absolute; bottom: 6px; left: 8px; cursor: pointer;';
  refreshButton.title = 'Syncing Conversations';
  refreshButton.innerHTML = '<svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#00aaff" d="M468.9 32.11c13.87 0 27.18 10.77 27.18 27.04v145.9c0 10.59-8.584 19.17-19.17 19.17h-145.7c-16.28 0-27.06-13.32-27.06-27.2c0-6.634 2.461-13.4 7.96-18.9l45.12-45.14c-28.22-23.14-63.85-36.64-101.3-36.64c-88.09 0-159.8 71.69-159.8 159.8S167.8 415.9 255.9 415.9c73.14 0 89.44-38.31 115.1-38.31c18.48 0 31.97 15.04 31.97 31.96c0 35.04-81.59 70.41-147 70.41c-123.4 0-223.9-100.5-223.9-223.9S132.6 32.44 256 32.44c54.6 0 106.2 20.39 146.4 55.26l47.6-47.63C455.5 34.57 462.3 32.11 468.9 32.11z"/></svg>';
  const syncDiv = document.createElement('div');
  syncDiv.classList = 'flex flex-1 flex-col';
  syncDiv.id = 'sync-div';
  syncDiv.style = 'max-height: 10px; opacity:1';
  syncDiv.appendChild(tooltip);
  syncDiv.appendChild(refreshButton);
  syncDiv.appendChild(progressLabel);
  syncDiv.appendChild(progressBar);
  nav.appendChild(syncDiv);
}
function resetProgressBar() {
  const progressBar = document.getElementById('sync-progressbar');
  const progressLabel = document.getElementById('sync-progresslabel');
  const tooltip = document.getElementById('sync-tooltip');
  if (progressBar && progressLabel && tooltip) {
    progressBar.style.backgroundColor = 'gold';
    progressBar.classList.remove('animate-pulse');
    progressLabel.innerText = 'Synced';

    tooltip.innerText = 'Your conversations are synced!';
  }
  const refreshButton = document.getElementById('sync-refresh-button');
  if (refreshButton) {
    refreshButton.title = 'Sync Conversations';
    refreshButton.classList.add('cursor-pointer');
    refreshButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="gold" d="M468.9 32.11c13.87 0 27.18 10.77 27.18 27.04v145.9c0 10.59-8.584 19.17-19.17 19.17h-145.7c-16.28 0-27.06-13.32-27.06-27.2c0-6.634 2.461-13.4 7.96-18.9l45.12-45.14c-28.22-23.14-63.85-36.64-101.3-36.64c-88.09 0-159.8 71.69-159.8 159.8S167.8 415.9 255.9 415.9c73.14 0 89.44-38.31 115.1-38.31c18.48 0 31.97 15.04 31.97 31.96c0 35.04-81.59 70.41-147 70.41c-123.4 0-223.9-100.5-223.9-223.9S132.6 32.44 256 32.44c54.6 0 106.2 20.39 146.4 55.26l47.6-47.63C455.5 34.57 462.3 32.11 468.9 32.11z"/></svg>';
    refreshButton.onclick = (e) => {
      // remove progress bar and refresh button and progress label

      const canSubmit = canSubmitPrompt() || document.querySelector('#conversation-regenerate-button');
      if (isGenerating || !canSubmit) return;
      const syncDiv = document.getElementById('sync-div');
      syncDiv.remove();
      const { pathname } = new URL(window.location.toString());
      const conversationId = pathname.split('/c/').pop().replace(/[^a-z0-9-]/gi, '');
      const refreshIds = [];
      if (/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(conversationId)) {
        refreshIds.push(conversationId);
      }
      // if shift + cmnd/ctrl
      if (e.shiftKey && (e.metaKey || (isWindows() && e.ctrlKey))) {
        chrome.storage.local.set({
          conversations: {},
          conversationsAreSynced: false,
        }, () => {
          window.location.reload();
        });
      } else {
        initializeAutoSave(true, refreshIds);
      }
    };
  }
}
function reloadOrAddRefreshButtonToSyncBanner(localConversations, settings, skipFullReload = false) {
  const existingSyncBanner = document.querySelector('#sync-nav-wrapper');
  const refreshButton = document.getElementById('sync-refresh-button');
  const textAreaElement = document.querySelector('#prompt-textarea');
  const modalWrapper = document.querySelector('[id^=modal-wrapper-]');
  const newPromptChainModal = document.querySelector('#new-prompt-chain-modal');
  const customInstructionNameInput = document.querySelector('#custom-instructions-name-input');
  const canSubmit = canSubmitPrompt();
  getConversations(0, 1).then((conversations) => {
    let shouldReload = false;
    const lastRemoteConversation = conversations.items[0];
    const lastLocalConversation = Object.values(localConversations).sort((a, b) => b.update_time - a.update_time)[0];
    if (lastRemoteConversation && lastLocalConversation && lastRemoteConversation.id !== lastLocalConversation.id) {
      shouldReload = true;
    }
    if ((settings.autoRefreshAfterSync || typeof settings.autoRefreshAfterSync === 'undefined') && textAreaElement && textAreaElement.value === '' && !modalWrapper && !customInstructionNameInput && !newPromptChainModal && canSubmit) {
      if (shouldReload) {
        window.location.reload();
      } else {
        existingSyncBanner.remove();
        loadConversationList(skipFullReload);
      }
    } else {
      // replace the content with "sync is complete" and a refresh button
      const pageRefreshButton = document.createElement('button');
      refreshButton.id = 'sync-page-refresh-button';
      pageRefreshButton.style = 'color: gold; cursor: pointer; border: solid 1px gold; padding: 8px; border-radius: 4px; margin-left: 16px;';
      pageRefreshButton.innerText = 'Refresh page';
      pageRefreshButton.addEventListener('click', () => {
        if (shouldReload) {
          window.location.reload();
        } else {
          existingSyncBanner.remove();
          loadConversationList(skipFullReload);
        }
      });
      setTimeout(() => {
        existingSyncBanner.firstChild.innerHTML = 'Sync is complete! Refresh the page to see enable all features.';
        existingSyncBanner.firstChild.appendChild(pageRefreshButton);
      }, 500);
    }
  });
}
function inSyncConversations(localConvs, remoteConvs) {
  return Object.keys(localConvs).filter(
    (id) => !localConvs[id].shouldRefresh
      && (formatTime(localConvs[id]?.update_time) === formatTime(remoteConvs.find((rc) => rc.id === id)?.update_time))
      && (typeof localConvs[id].saveHistory === 'undefined' || localConvs[id].saveHistory),
  );
}
function updateProgressBar(localConvs, remoteConvs) {
  const progressLabel = document.getElementById('sync-progresslabel');
  if (progressLabel) {
    // eslint-disable-next-line no-loop-func
    progressLabel.innerText = `Syncing(${inSyncConversations(localConvs, remoteConvs).length}/${Object.keys(remoteConvs).length})`;
    if (remoteConvs.length > 0 && remoteConvs.length - inSyncConversations(localConvs, remoteConvs).length > 5) {
      addSyncBanner();
    }
  }
}

function removeDuplicateConversationIds(conversationsOrder) {
  const conversationsOrderIds = conversationsOrder.filter((conv) => (typeof conv === 'string'));
  const folders = conversationsOrder.filter((conv) => typeof conv === 'object');
  // remove duplicates from conversationsOrderIds
  const newConversationsOrderIds = [...new Set(conversationsOrderIds)];
  // remove duplicates from folders
  folders.forEach((folder) => {
    folder.conversationIds = [...new Set(folder?.conversationIds)];
  });
  // ---------------------------------------
  // combine folders with same id into one and remove duplicates
  const newFolders = [];
  folders.forEach((folder) => {
    const existingFolder = newFolders.find((f) => f?.id === folder?.id);
    if (existingFolder) {
      existingFolder.conversationIds = [...new Set([...existingFolder.conversationIds, ...folder.conversationIds])];
    } else {
      newFolders.push(folder);
    }
  });
  // ---------------------------------------
  // remove anything in folders from newConversationsOrderIds
  newFolders.forEach((folder) => {
    folder.conversationIds.forEach((convId) => {
      if (newConversationsOrderIds.includes(convId)) {
        newConversationsOrderIds.splice(newConversationsOrderIds.indexOf(convId), 1);
      }
    });
  });
  // ---------------------------------------
  // remove anything in folders from other folders
  newFolders.forEach((folder) => {
    newFolders.forEach((f) => {
      if (f.id !== folder.id) {
        f.conversationIds = f.conversationIds.filter((convId) => !folder.conversationIds.includes(convId));
      }
    });
  });

  return [...newFolders, ...newConversationsOrderIds];
}

function deleteFromConversationsOrder(conversationsOrder, convId) {
  const newConversationsOrder = conversationsOrder || [];
  // check conversations
  if (newConversationsOrder.indexOf(convId) !== -1) {
    newConversationsOrder.splice(newConversationsOrder.indexOf(convId), 1);
  } else {
    // check folders
    // eslint-disable-next-line no-loop-func
    newConversationsOrder.forEach((folder) => {
      if (typeof folder === 'object' && folder?.conversationIds.indexOf(convId) !== -1) {
        folder?.conversationIds.splice(folder.conversationIds.indexOf(convId), 1);
      }
    });
  }

  return newConversationsOrder;
}

// eslint-disable-next-line no-unused-vars
function initializeAutoSave(skipFullReload = false, forceRefreshIds = []) {
  clearTimeout(autoSaveTimeoutId);
  addProgressBar();

  const forceRefresh = true;
  getAllConversations(forceRefresh).then((remoteConversations) => {
    chrome.storage.local.get(['conversationsOrder', 'conversations', 'settings'], (result) => {
      const { settings, conversationsOrder } = result;
      let localConversations = {};
      if (result.conversations && Object.keys(result.conversations).length > 0) {
        localConversations = result.conversations;
      }

      let newConversationsOrder = conversationsOrder || [];
      // remove trash folder from newConversationsOrder
      newConversationsOrder = newConversationsOrder.filter((conv) => typeof conve === 'string' || conv?.id !== 'trash');
      chrome.storage.local.set({
        conversationsAreSynced: false,
        conversationsOrder: newConversationsOrder,
        conversations: localConversations,
      }, async () => {
        loadConversationList(skipFullReload);

        const remoteConvIds = remoteConversations.map((conv) => conv?.id);
        const localConvIds = Object.keys(localConversations);
        // update existing conversations
        for (let i = 0; i < localConvIds.length; i += 1) {
          if (localConversations[localConvIds[i]]?.saveHistory === false) continue;
          const remoteConv = remoteConversations.find((conv) => conv?.id === localConvIds[i]);
          if (!remoteConv) {
            delete localConversations[localConvIds[i]];
          } else {
            localConversations[localConvIds[i]].title = remoteConv?.title;
            if (
              forceRefreshIds.includes(localConvIds[i])
              || localConversations[localConvIds[i]]?.update_time === 'force_copy'
              || localConversations[localConvIds[i]]?.shouldRefresh
              || formatTime(localConversations[localConvIds[i]]?.update_time) !== formatTime(remoteConv.update_time)) {
              // if conversation was updated on another device, or shouldRefresh=True update it
              localConversations = await updateConversationInStorage(localConversations, localConvIds[i]);
            }
          }
        }
        // save local conversations to storage to lose progress
        chrome.storage.local.set({
          conversations: localConversations,
        });
        // load non-synced state
        if (remoteConvIds.length > 0 && (remoteConvIds.length - inSyncConversations(localConversations, remoteConversations).length) > 5) {
          // initializeTimestamp();
          // updateNewChatButtonNotSynced();
          // addAsyncInputEvents();
          addSyncBanner();
        }
        // Add missing conversations from remote to local
        for (let i = 0; i < remoteConvIds.length; i += 1) {
          if (!localConvIds.includes(remoteConvIds[i])) {
            localConversations = await addConversationToStorage(localConversations, remoteConvIds[i]);
            // update progress bar
            updateProgressBar(localConversations, remoteConversations);
            // await autoSaveCountDownAsync();
          }
        }
        // update conversationsOrder based on localConversations
        const newLocalConvIds = Object.keys(localConversations);
        const allConversationsOrderIds = newConversationsOrder.map((conv) => (typeof conv === 'object' ? conv?.conversationIds : conv)).flat();
        // find ids that exist in conversationsOrder but not in localConversations
        const extraConversationsOrderIds = allConversationsOrderIds.filter((id) => !newLocalConvIds.includes(id));
        // remove extraConversationsOrderIds from conversationsOrder
        for (let i = 0; i < extraConversationsOrderIds.length; i += 1) {
          newConversationsOrder = deleteFromConversationsOrder(newConversationsOrder, extraConversationsOrderIds[i], false);
        }
        // add missing conversations from remoteconvIds to conversationsOrder
        for (let i = 0; i < remoteConvIds.length; i += 1) {
          if (!allConversationsOrderIds.includes(remoteConvIds[i])) {
            newConversationsOrder.unshift(remoteConvIds[i]);
          }
        }
        // remove duplicate convids from newConversationsOrder and remove duplicates from conversationsIds in each folder
        newConversationsOrder = removeDuplicateConversationIds(newConversationsOrder);
        // sort conversations by updated time
        newConversationsOrder = sortConversationsByTimestamp(newConversationsOrder, localConversations, settings);
        // save everything to storage
        chrome.storage.local.set({
          conversations: localConversations,
          conversationsAreSynced: true,
          conversationsOrder: newConversationsOrder,
        }, () => {
          resetProgressBar();
          const existingSyncBanner = document.querySelector('#sync-nav-wrapper');
          if (existingSyncBanner) {
            reloadOrAddRefreshButtonToSyncBanner(localConversations, settings, true);
          } else {
            loadConversationList(true);
          }
        });
      });
    });
  }, () => {
    // if the conversation history endpoint failed, set conversationsAreSynced to true
    chrome.storage.local.set({
      conversationsAreSynced: true,
    }, () => {
      resetProgressBar();
      loadConversationList(true);
    });
  });
}

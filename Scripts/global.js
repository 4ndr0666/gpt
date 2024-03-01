/* global markdownit, hljs, getAccount, createSettingsModal, isAltKeyDown */

/* eslint-disable no-unused-vars */

//------------------------------------------------------------------------------------------------
// eslint-disable-next-line prefer-const
let isGenerating = false;// true when the user is generating a response
// eslint-disable-next-line prefer-const
let chatStreamIsClosed = false; // to force close the chat stream
// eslint-disable-next-line prefer-const
let shiftKeyPressed = false;

// chrome.storage.onChanged.addListener((changes, namespace) => {
//   // eslint-disable-next-line no-restricted-syntax
//   for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
//     // eslint-disable-next-line no-console
//     if (key !== 'conversations') {
//       console.warn({
//         key,
//         namespace,
//         oldValue,
//         newValue,
//       });
//     }
//   }
// });
function isWindows() {
  return navigator.platform.indexOf('Win') > -1;
}
function openLinksInNewTab() {
  const base = document.createElement('base');
  base.target = '_blank';
  document.head.appendChild(base);
}
function initializeStorage() {
  // clear storage
  // chrome.storage.local.clear();
  // chrome.storage.sync.clear();
  // print storage
  // chrome.storage.sync.get(null, (items) => {
  //   const allKeys = Object.keys(items);
  //   console.log('sync', items);
  // });
  // chrome.storage.local.get(null, (items) => {
  //   const allKeys = Object.keys(items);
  //   console.log('local', items);
  // });
  chrome.storage.local.get(['account'], ({ account }) => {
    chrome.storage.onChanged.addListener((e) => {
      if (e.conversations) {
        if (account?.account_ordering?.length > 1) {
          chrome.storage.local.get([
            'chatgptAccountId', 'allConversations', 'conversations',
          ], (res) => {
            const {
              chatgptAccountId, allConversations, conversations,
            } = res;
            chrome.storage.local.set({
              allConversations: { ...allConversations, [chatgptAccountId]: conversations },
            });
          });
        }
      }
      if (e.conversationsOrder) {
        // get all folders
        const folders = e.conversationsOrder.newValue.filter((convOrFold) => typeof convOrFold !== 'string');
        // for each folder get the conversationIds
        const conversationIds = folders.map((folder) => folder.conversationIds);
        // flatten the conversationIds
        const flattenedConversationIds = conversationIds.flat();
        // if conversationIds are not strings (they are objects), get the id property
        flattenedConversationIds.forEach((conversationId, index) => {
          if (typeof conversationId !== 'string') {
            // eslint-disable-next-line no-console
            console.warn('Bad type. Please contact the developer!');
          }
        });

        // if there are duplicates, remove them
        const uniqueConversationIds = [...new Set(flattenedConversationIds)];
        if (uniqueConversationIds.length !== flattenedConversationIds.length) {
          // eslint-disable-next-line no-console
          console.warn('Not unique. Please contact the developer!');
        }

        if (account?.account_ordering?.length > 1) {
          // update allConversationsOrder
          chrome.storage.local.get([
            'chatgptAccountId', 'allConversationsOrder', 'conversationsOrder',
          ], (res) => {
            const {
              chatgptAccountId, allConversationsOrder, conversationsOrder,
            } = res;
            chrome.storage.local.set({
              allConversationsOrder: { ...allConversationsOrder, [chatgptAccountId]: conversationsOrder },
            });
          });
        }
      }
    });
  });
  return chrome.storage.local.get(['customModels']).then((result) => chrome.storage.local.set({
    selectedConversations: [],
    lastSelectedConversation: null,
    customModels: result.customModels || [],
    unofficialModels: [
      {
        title: 'gpt-3.5-turbo-1106',
        description: 'The latest GPT-3.5 Turbo model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more.',
        slug: 'gpt-3.5-turbo-1106',
        tags: ['Unofficial'],
      },
      {
        title: 'gpt-4-1106-preview',
        description: 'The latest GPT-4 model with improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more.',
        slug: 'gpt-4-1106-preview',
        tags: ['Unofficial'],
      },
      {
        title: 'gpt-4-32k',
        description: 'Currently points to gpt-4-32k-0613.',
        slug: 'gpt-4-32k',
        tags: ['Unofficial'],
      },
    ],
  }));
}
// eslint-disable-next-line new-cap
const markdown = (role) => new markdownit({
  html: role === 'assistant',
  linkify: true,
  highlight(str, _lang) {
    const { language, value } = hljs.highlightAuto(str);
    return `<pre dir="ltr" class="w-full"><div class="bg-black mb-4 rounded-md"><div id='code-header' class="flex items-center relative text-token-text-tertiary ${role === 'user' ? 'bg-gray-900' : 'bg-gray-800'} px-4 py-2 text-xs font-sans rounded-t-md" style='border-top-left-radius:6px;border-top-right-radius:6px;'><span class="">${language}</span><button id='copy-code' data-initialized="false" class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-${language}">${value}</code></div></div></pre>`;
  },
});
function addSounds() {
  const audio = document.createElement('audio');
  audio.id = 'beep-sound';
  audio.src = chrome.runtime.getURL('sounds/beep.mp3');
  document.body.appendChild(audio);
}
function playSound(sound) {
  const audio = document.getElementById(`${sound}-sound`);
  audio.play();
}

function escapeHtml(html) {
  return html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
function addDevIndicator() {
  chrome.storage.local.get('API_URL', ({ API_URL }) => {
    if (API_URL?.includes('dev')) {
      const devIndicator = document.createElement('div');
      devIndicator.style = 'position:fixed;bottom:16px;right:16px;z-index:9000;background-color:#19c37d;width:4px;height:4px;border-radius:100%;';
      document.body.appendChild(devIndicator);
    }
  });
}
const debounce = (func, wait = 1000) => {
  let timeout;

  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};
let scrolUpDetected = false;
function addScrollDetector(element) {
  let lastScrollTop = element.scrollTop;
  scrolUpDetected = false;
  element.addEventListener('scroll', () => { // or window.addEventListener("scroll"....
    const st = element.scrollTop; // Credits: "https://github.com/qeremy/so/blob/master/so.dom.js#L426"
    if (st > lastScrollTop) {
      // downscroll code
      // if reached the end of the page set scrolUpDetected to false
      if (element.scrollHeight - element.scrollTop === element.clientHeight) {
        scrolUpDetected = false;
      }
    } else if (st < lastScrollTop - 3) { // 20 is the threshold
      // upscroll code
      scrolUpDetected = true;
    } // else was horizontal scroll
    lastScrollTop = st <= 0 ? 0 : st; // For Mobile or negative scrolling
  }, false);
}

const copyRichText = (element) => {
  let content = element.cloneNode(true);
  // remove all div with id=code-header from content
  const codeHeader = content.querySelectorAll('#code-header');
  codeHeader.forEach((header) => {
    header.remove();
  });
  content = content.innerHTML.trim();
  const clipboardItem = new ClipboardItem({
    'text/html': new Blob(
      [content],
      { type: 'text/html' },
    ),
    'text/plain': new Blob(
      [content],
      { type: 'text/plain' },
    ),
  });
  navigator.clipboard.write([clipboardItem]);
};
function removeGrammerly() {
  const grammarlyExtension = document.querySelectorAll('grammarly-extension');
  grammarlyExtension?.forEach((g) => g.remove());
}
function convertNumberToHumanReadable(number) {
  if (!number) return 0;
  if (number === 0) return number;

  const SI_SYMBOL = ['', 'k', 'M', 'G', 'T', 'P', 'E'];
  // eslint-disable-next-line no-bitwise
  const tier = Math.log10(number) / 3 | 0;
  if (tier === 0) return number;
  const suffix = SI_SYMBOL[tier];
  const scale = 10 ** (tier * 3);
  const scaled = number / scale;
  return scaled.toFixed(1) + suffix;
}
function showAutoSyncWarning(settings) {
  if (settings?.dontShowAutoSyncWarning) return;
  const existingAutoSyncWarning = document.getElementById('confirm-action-dialog');
  if (existingAutoSyncWarning) return;
  showConfirmDialog('Welcome to Superpower ChatGPT 👋', 'Glad to have you here. If you have any questions, please feel free to <b><a target="_blank" style="text-decoration:underline; color:gold;" href="mailto:support@superpowerdaily.com?subject=I have a question">email us</a></b> or join our <b><a target="_blank" style="text-decoration:underline; color:gold;" href="https://discord.gg/superpower-chatgpt-1083455984489476220">Discord</a></b> channel for faster support.<br/><br/>Want to learn more? Check out our <b><a style="text-decoration:underline; color:gold;" href="https://www.youtube.com/@superpowerdaily" target="blank">YouTube</a></b> channel where you can find lots of useful guides on how to use SUperpower ChatGPT<br/><br/>', '⚡️ Enable AutoSync', null, () => confirmAutoSync(settings), 'green', true, (checked) => doNotShowAutoSyncWarningAgainCallback(settings, checked));
}
function confirmAutoSync(settings) {
  chrome.storage.local.set({ settings: { ...settings, autoSync: true } }, () => {
    window.location.reload();
  });
}
function doNotShowAutoSyncWarningAgainCallback(settings, checked) {
  chrome.storage.local.set({ settings: { ...settings, dontShowAutoSyncWarning: checked } });
}
function switchFavicon() {
  if (typeof switchFavicon.i === 'undefined') {
    switchFavicon.i = 0;
  }
  switch (switchFavicon.i) {
    case 0:
      changeFavicon(chrome.runtime.getURL('icons/favicon-1.png'));
      break;
    case 1:
      changeFavicon(chrome.runtime.getURL('icons/favicon-0.png'));
      break;
    default:
      changeFavicon(chrome.runtime.getURL('icons/favicon-0.png'));
  }
  switchFavicon.i = switchFavicon.i === 1 ? 0 : 1;
}
function animateFavicon() {
  const faviconTimeout = setInterval(switchFavicon, 500);
  return faviconTimeout;
}
function stopAnimateFavicon(faviconTimeout) {
  changeFavicon(chrome.runtime.getURL('icons/favicon-0.png'));
  clearTimeout(faviconTimeout);
}
function changeFavicon(src) {
  const link = document.createElement('link');
  // anything with rel=icon is removed by the browser
  const oldLinks = document.querySelectorAll('link[rel="icon"]');
  link.rel = 'icon';
  link.type = 'image/gif';
  link.href = src;
  if (oldLinks) {
    oldLinks.forEach((oldLink) => {
      if (oldLink.href.includes('favicon')) {
        document.head.removeChild(oldLink);
      }
    });
  }
  document.head.appendChild(link);
}
function addScrollButtons() {
  const observer = new MutationObserver(() => {
    const existingScrollButtonWrapper = document.getElementById('scroll-button-wrapper');
    const textAreaElement = document.querySelector('#prompt-textarea');
    if (!textAreaElement) {
      if (existingScrollButtonWrapper) existingScrollButtonWrapper.remove();
      return;
    }
    if (existingScrollButtonWrapper) return;

    const scrollButtonWrapper = document.createElement('div');
    scrollButtonWrapper.id = 'scroll-button-wrapper';
    scrollButtonWrapper.classList = 'absolute flex items-center justify-center text-xs font-sans cursor-pointer rounded-md z-10';
    scrollButtonWrapper.style = 'bottom: 6rem;right: 3rem;width: 2rem;flex-wrap:wrap;';
    const scrollUpButton = document.createElement('button');
    scrollUpButton.id = 'scroll-up-button';
    scrollUpButton.innerHTML = '<svg stroke="currentColor" fill="none" stroke-width="4" viewBox="0 0 48 48" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M24 44V4m20 20L24 4 4 24"></path></svg>';
    scrollUpButton.classList = 'flex items-center justify-center border-black/10 dark:border-gray-900/50 hover:text-token-text-primary text-token-text-secondary text-xs font-sans cursor-pointer rounded-t-md z-10 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-900';
    scrollUpButton.style = 'width: 2rem;height: 2rem;border: 1px solid;';
    scrollUpButton.addEventListener('click', () => {
      const curConversationTop = document.querySelector('[id^=message-wrapper-]');
      if (!curConversationTop) return;
      curConversationTop.parentElement.scrollIntoView({ behavior: 'smooth' });
    });

    const scrollDownButton = document.createElement('button');
    scrollDownButton.id = 'scroll-down-button';
    scrollDownButton.innerHTML = '<svg stroke="currentColor" fill="none" stroke-width="4" viewBox="0 0 48 48" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M24 4v40M4 24l20 20 20-20"></path></svg>';
    scrollDownButton.classList = 'flex items-center justify-center border-black/10 dark:border-gray-900/50 hover:text-token-text-primary text-token-text-secondary text-xs font-sans cursor-pointer rounded-b-md z-10 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-900';
    scrollDownButton.style = 'width: 2rem;height: 2rem;border: 1px solid; border-top: none;';
    scrollDownButton.addEventListener('click', () => {
      const curConversationBottom = document.querySelector('#conversation-bottom');

      if (!curConversationBottom) return;
      curConversationBottom.scrollIntoView({ behavior: 'smooth' });
    });

    scrollButtonWrapper.appendChild(scrollUpButton);
    scrollButtonWrapper.appendChild(scrollDownButton);

    document.body.appendChild(scrollButtonWrapper);
  });

  const main = document.querySelector('main');
  if (!main) return;
  observer.observe(main, {
    childList: true,
    subtree: true,
  });
}
// eslint-disable-next-line no-unused-vars
function showConfirmDialog(title, subtitle, confirm, cancelCallback, confirmCallback, confirmType = 'red', closeOnConfirm = true, doNotShowAgainCallback = false) { // confirmType: red, orange, green
  const existingConfirmActionDialog = document.getElementById('confirm-action-dialog');
  if (existingConfirmActionDialog) existingConfirmActionDialog.remove();
  const bottonColors = {
    red: 'btn-danger',
    orange: 'btn-warning',
    green: 'btn-primary',
  };
  const confirmActionDialog = `<div data-state="open" class="fixed inset-0 bg-black/50 dark:bg-gray-600/70" style="pointer-events: auto;"><div class="grid-cols-[10px_1fr_10px] grid h-full w-full grid-rows-[minmax(10px,_1fr)_auto_minmax(10px,_1fr)] md:grid-rows-[minmax(20px,_1fr)_auto_minmax(20px,_1fr)] overflow-y-auto"><div id="confirm-action-dialog-content" role="dialog" id="radix-:r3m:" aria-describedby="radix-:r3o:" aria-labelledby="radix-:r3n:" data-state="open" class="relative col-auto col-start-2 row-auto row-start-2 w-full rounded-xl text-left shadow-xl transition-all left-1/2 -translate-x-1/2 bg-white dark:bg-gray-900 max-w-xl" tabindex="-1" style="pointer-events: auto;"><div class="px-4 pb-4 pt-5 sm:p-6 flex items-center justify-between border-b border-black/10 dark:border-white/10"><div class="flex"><div class="flex items-center"><div class="flex grow flex-col gap-1"><h2 id="radix-:r3n:" as="h3" class="text-lg font-medium leading-6 text-token-text-secondary">${title}</h2></div></div></div></div><div class="p-4 sm:p-6"><div class="text-sm">${subtitle}</div><div class="mt-5 sm:mt-4"><div class="mt-5 flex sm:mt-4 justify-between">${doNotShowAgainCallback ? '<div style="display: flex; justify-content: flex-start; align-items: center;"><input type="checkbox" id="do-not-show-checkbox" style="margin-right: 8px; width: 12px; height: 12px;" /><label for="do-not-show-checkbox" class="text-sm text-token-text-secondary">Do not show again</label></div>' : ''}<div class="flex sm:flex-row-reverse gap-3 ml-auto"><button id="confirm-button" class="btn relative ${bottonColors[confirmType]}" as="button"><div class="flex w-full gap-2 items-center justify-center">${confirm}</div></button><button id="cancel-button" class="btn relative btn-neutral" as="button"><div class="flex w-full gap-2 items-center justify-center">Cancel</div></button></div></div></div></div></div></div></div></div>`;
  const confirmActionDialogElement = document.createElement('div');
  confirmActionDialogElement.id = 'confirm-action-dialog';
  confirmActionDialogElement.classList = 'absolute inset-0';
  confirmActionDialogElement.style = 'z-index: 10000;';
  confirmActionDialogElement.innerHTML = confirmActionDialog;
  document.body.appendChild(confirmActionDialogElement);
  const confirmButton = document.querySelector('#confirm-action-dialog #confirm-button');
  const cancelButton = document.querySelector('#confirm-action-dialog #cancel-button');
  confirmButton.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const curConfirmButton = document.querySelector('#confirm-action-dialog #confirm-button');
    if (curConfirmButton?.querySelector('#progress-spinner')) return;
    if (confirmCallback) confirmCallback();
    if (closeOnConfirm) {
      confirmActionDialogElement.remove();
    }
  });
  cancelButton.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    const curConfirmButton = document.querySelector('#confirm-action-dialog #confirm-button');
    if (curConfirmButton?.querySelector('#progress-spinner')) return;

    if (cancelCallback) cancelCallback();
    confirmActionDialogElement.remove();
  });
  // click outside to close
  confirmActionDialogElement.addEventListener('click', (e) => {
    const curConfirmButton = document.querySelector('#confirm-action-dialog #confirm-button');
    if (curConfirmButton.querySelector('#progress-spinner')) return;
    const confirmActionDialogContent = document.querySelector('#confirm-action-dialog-content');
    if (!isDescendant(confirmActionDialogContent, e.target)) {
      confirmActionDialogElement.remove();
    }
  });
  // press escape to close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      cancelButton.click();
    }
  });
  // do not show again
  const doNotShowAgainCheckbox = document.querySelector('#do-not-show-checkbox');
  if (doNotShowAgainCheckbox) {
    doNotShowAgainCheckbox.addEventListener('change', (e) => {
      const { checked } = doNotShowAgainCheckbox;
      if (doNotShowAgainCallback) doNotShowAgainCallback(checked);
    });
  }
}
function closeMenusEventListener() {
  document.body.addEventListener('click', () => closeMenus());
}
function closeMenus() {
  let menus = document.querySelectorAll('#sidebar-gizmo-menu');
  if (menus.length > 0) menus.forEach((menu) => menu.remove());
  menus = document.querySelectorAll('#selected-conversations-action-menu');
  if (menus.length > 0) menus.forEach((menu) => menu.remove());
  menus = document.querySelectorAll('#folder-element-menu');
  if (menus.length > 0) menus.forEach((menu) => menu.remove());
  menus = document.querySelectorAll('#sidebar-gizmo-menu');
  if (menus.length > 0) menus.forEach((menu) => menu.remove());
  menus = document.querySelectorAll('#conversation-element-menu');
  if (menus.length > 0) menus.forEach((menu) => menu.remove());
  menus = document.querySelectorAll('#more-categories-menu');
  if (menus.length > 0) menus.forEach((menu) => menu.remove());
}
function getGizmoIdFromUrl(defaultURL = null) {
  const url = defaultURL || window.location.href;
  const pattern = /\/g\/(g-[A-Za-z0-9]+)/;

  const match = url.match(pattern);
  if (match) {
    const group = match[1];
    return group;
  }
  return null;
}

function replacePageContent(newContent) {
  const presentation = document.querySelector('main > div[role=presentation]');
  if (!presentation) return;
  presentation.classList = 'flex h-full flex-col';

  const contentWrapper = presentation?.firstChild;
  // div with class flex-1 overflow-hidden
  contentWrapper.innerHTML = '';
  contentWrapper.id = 'content-wrapper';
  contentWrapper.classList = 'flex-1 overflow-hidden';
  contentWrapper.appendChild(newContent);
}
function generateRandomDarkColor() {
  // Generate random values for RGB, keeping them below 100 to ensure darkness
  const color1 = Math.floor(Math.random() * 180);
  const color2 = Math.floor(Math.random() * 180);
  const color3 = Math.floor(Math.random() * 180);
  // shuffle the colors and set r,g,b equal to them
  const colors = [color1, color2, color3];
  colors.sort(() => Math.random() - 0.5);
  const r = colors[0];
  const g = colors[1];
  const b = colors[2];
  // Convert the color to a hexadecimal format
  const color = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;

  return color;
}
function handleQueryParams(query) {
  const urlParams = new URLSearchParams(query);
  const promptId = urlParams.get('pid');
  if (promptId) {
    chrome.runtime.sendMessage({
      getPrompt: true,
      detail: {
        promptId,
      },
    }, (prompt) => {
      const textAreaElement = document.querySelector('#prompt-textarea');
      textAreaElement.value = prompt.text;
      textAreaElement.focus();
      textAreaElement.dispatchEvent(new Event('input', { bubbles: true }));
      textAreaElement.dispatchEvent(new Event('change', { bubbles: true }));
    });
  }
}

function getMousePosition(event) {
  const x = event.clientX;
  const y = event.clientY;
  return { x, y };
}
function isDescendant(parent, child) {
  let node = child?.parentNode;
  while (node != null) {
    if (node === parent) {
      return true;
    }
    node = node.parentNode;
  }
  return false;
}

function getBrowser() {
  if (typeof chrome !== 'undefined') {
    if (typeof browser !== 'undefined') {
      return 'Firefox';
    }
    return 'Chrome';
  }
  return 'Edge';
}

function initializeAutoRefreshAccount() {
  setInterval(() => {
    chrome.storage.sync.get(['accessToken']).then((res) => {
      if (!res.accessToken) return;
      chrome.storage.local.get(['lastAccountRefresh'], (result) => {
        const lastAccountRefresh = result.lastAccountRefresh || 0;
        getAccount();
      });
    });
  }, 1000 * 60 * 25); // refresh account every 25 minutes
}

function formatTime(time) {
  if (!time) return time;
  // if time in format "2023-11-11T21:37:10.479788+00:00"
  if (time.toString().indexOf('T') !== -1) {
    return new Date(time).getTime();
  }
  // if time in format 1699691863.236379 (10 digits before dot)
  if (time.toString().indexOf('.') !== -1 && time.toString().split('.')[0].length === 10) {
    return new Date(time * 1000).getTime();
  }
  // if time in format 1699691863236.379 (13 digits before dot)
  if (time.toString().indexOf('.') !== -1 && time.toString().split('.')[0].length === 13) {
    return new Date(time).getTime();
  }
  // if time is 10 digit
  if (time.toString().length === 10) {
    return new Date(time * 1000).getTime();
  }

  return time;
}

function formatDate(date) {
  if (!date) return date;
  // if date is today show hh:mm. if older than today just show date yyyy-mm-dd
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const todayDate = today.getDate();
  const todayMonth = today.getMonth() + 1;
  const todayYear = today.getFullYear();
  const dateDate = date.getDate();
  const dateMonth = date.getMonth() + 1;
  const dateYear = date.getFullYear();
  if (todayDate === dateDate && todayMonth === dateMonth && todayYear === dateYear) {
    return `Today ${date.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric' })}`;
  }
  if (yesterday.getDate() === dateDate && yesterday.getMonth() + 1 === dateMonth && yesterday.getFullYear() === dateYear) {
    return `Yesterday ${date.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric' })}`;
  }
  return `${date.toLocaleDateString('en-US', { year: '2-digit', month: '2-digit', day: '2-digit' })} ${date.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric' })}`;
}
function formatDateDalle() { // 2023-12-02 22.47.07
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  const month = String(currentDate.getMonth() + 1).padStart(2, '0'); // January is 0
  const day = String(currentDate.getDate()).padStart(2, '0');
  const hours = String(currentDate.getHours()).padStart(2, '0');
  const minutes = String(currentDate.getMinutes()).padStart(2, '0');
  const seconds = String(currentDate.getSeconds()).padStart(2, '0');

  const formattedDate = `${year}-${month}-${day} ${hours}.${minutes}.${seconds}`;
  return formattedDate;
}

function removeMarkTagsInsideBackticks(input) {
  const pattern = /(`{1,3})([^`]*?)\1/gs;
  return input.replace(pattern, (match, backticks, codeBlock) => {
    const codeWithoutMarkTags = codeBlock.replace(/<\/?mark>/gi, '');
    return backticks + codeWithoutMarkTags + backticks;
  });
}
function addAutoSyncToggleButton() {
  const existingAutoSyncToggleButton = document.getElementById('auto-sync-toggle-button');
  if (existingAutoSyncToggleButton) existingAutoSyncToggleButton.remove();

  const autoSyncToggleButton = document.createElement('button');
  autoSyncToggleButton.id = 'keyboard-shortcuts-modal-button';
  autoSyncToggleButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" height="1.5em" viewBox="0 0 512 512" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="0" fill="currentColor"><path d="M256 79.1C178.5 79.1 112.7 130.1 89.2 199.7C84.96 212.2 71.34 218.1 58.79 214.7C46.23 210.5 39.48 196.9 43.72 184.3C73.6 95.8 157.3 32 256 32C337.5 32 408.8 75.53 448 140.6V104C448 90.75 458.7 80 472 80C485.3 80 496 90.75 496 104V200C496 213.3 485.3 224 472 224H376C362.7 224 352 213.3 352 200C352 186.7 362.7 176 376 176H412.8C383.7 118.1 324.4 80 256 80V79.1zM280 263.1C280 277.3 269.3 287.1 256 287.1C242.7 287.1 232 277.3 232 263.1V151.1C232 138.7 242.7 127.1 256 127.1C269.3 127.1 280 138.7 280 151.1V263.1zM224 352C224 334.3 238.3 319.1 256 319.1C273.7 319.1 288 334.3 288 352C288 369.7 273.7 384 256 384C238.3 384 224 369.7 224 352zM40 432C26.75 432 16 421.3 16 408V311.1C16 298.7 26.75 287.1 40 287.1H136C149.3 287.1 160 298.7 160 311.1C160 325.3 149.3 336 136 336H99.19C128.3 393 187.6 432 256 432C333.5 432 399.3 381.9 422.8 312.3C427 299.8 440.7 293 453.2 297.3C465.8 301.5 472.5 315.1 468.3 327.7C438.4 416.2 354.7 480 256 480C174.5 480 103.2 436.5 64 371.4V408C64 421.3 53.25 432 40 432V432z"/></svg>';
  autoSyncToggleButton.classList = 'absolute flex items-center justify-center bg-gray-100 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-900 text-xs font-sans cursor-pointer rounded-md z-10';
  autoSyncToggleButton.style = 'bottom: 6rem;right: 3rem;width: 2rem;height: 2rem;flex-wrap:wrap;border: 1px solid;color:#e06c2b';
  autoSyncToggleButton.title = 'Auto Sync is OFF. Click to turn ON';
  autoSyncToggleButton.addEventListener('click', () => {
    chrome.storage.local.get(['settings'], ({ settings }) => {
      chrome.storage.local.set({ settings: { ...settings, autoSync: true } }, () => {
        window.location.reload();
      });
    });
  });
  document.body.appendChild(autoSyncToggleButton);
}
function highlightSearch(elements, searchTerm) {
  debounce(highlightSearchDebounced, 500)(elements, searchTerm);
}
function highlightSearchDebounced(elements, searchTerm) {
  if (!elements) return;
  if (!searchTerm) {
    CSS.highlights.clear();
    return;
  }
  // Find all text nodes in the element. We'll search within
  // these text nodes.
  const allTextNodes = [];
  for (let i = 0; i < elements.length; i += 1) {
    if (!elements[i]) continue;
    const treeWalker = document.createTreeWalker(elements[i], NodeFilter.SHOW_TEXT);
    let currentNode = treeWalker.nextNode();
    while (currentNode) {
      allTextNodes.push(currentNode);
      currentNode = treeWalker.nextNode();
    }
  }
  // If the CSS Custom Highlight API is not supported,
  // display a message and bail-out.
  if (!CSS.highlights) {
    return;
  }

  // Clear the HighlightRegistry to remove the
  CSS.highlights.clear();

  // Clean-up the search query and bail-out if
  // if it's empty.
  const str = searchTerm.trim().toLowerCase();
  if (!str) {
    return;
  }

  // Iterate over all text nodes and find matches.
  const ranges = allTextNodes
    .map((el) => ({ el, text: el.textContent.toLowerCase() }))
    .map(({ text, el }) => {
      const indices = [];
      let startPos = 0;
      while (startPos < text.length) {
        const index = text.indexOf(str, startPos);
        if (index === -1) break;
        indices.push(index);
        startPos = index + str.length;
      }

      // Create a range object for each instance of
      // str we found in the text node.
      return indices.map((index) => {
        const range = new Range();
        range.setStart(el, index);
        range.setEnd(el, index + str.length);
        return range;
      });
    });

  // Create a Highlight object for the ranges.
  // eslint-disable-next-line no-undef
  const searchResultsHighlight = new Highlight(...ranges.flat());
  // Register the Highlight object in the registry.
  CSS.highlights.set('search-results', searchResultsHighlight);
}
function highlightBracket(text) {
  if (text.trim().length === 0) return '';
  // replace brackets [] and text between them with <mark> tag and remove the brackets
  return text.replace(/\{\{.*?\}\}/g, (match) => `<strong style="margin:0 2px; padding:1px 4px; border-radius:4px; background-color:#444554; font-style:italic; border:solid 1px gold;">${match.replace(/[{}]/g, '')}</strong>`);
}
function downloadFileFrmoUrl(url, filename) {
  fetch(url).then((response) => response.blob()).then((blob) => {
    const blobURL = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobURL;
    a.style.display = 'none';
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  });
}
// function downloadFilesAsZip(urls, filenames) {
//   const zip = new JSZip();
//   const folder = zip.folder('chatgpt-images');
//   urls.forEach((url, index) => {
//     fetch(url).then((response) => response.blob()).then((blob) => {
//       folder.file(filenames[index], blob);
//     });
//   });
//   zip.generateAsync({ type: 'blob' }).then((content) => {
//     const blobURL = URL.createObjectURL(content);
//     const a = document.createElement('a');
//     a.href = blobURL;
//     a.style.display = 'none';
//     a.download = 'chatgpt-images.zip';
//     document.body.appendChild(a);
//     a.click();
//     a.remove();
//   });
// }
function toast(html, type = 'info', duration = 4000) {
  // show toast that text is copied to clipboard
  const existingToast = document.querySelector('#gptx-toast');
  if (existingToast) existingToast.remove();
  const element = document.createElement('div');
  element.id = 'gptx-toast';
  element.style = 'position:fixed;right:24px;top:24px;border-radius:4px;background-color:#19c37d;padding:8px 16px;z-index:100001;max-width:600px;';
  if (type === 'error') {
    element.style.backgroundColor = '#ef4146';
  }
  if (type === 'warning') {
    element.style.backgroundColor = '#e06c2b';
  }
  element.innerHTML = html;
  document.body.appendChild(element);
  setTimeout(
    () => {
      if (!isAltKeyDown) {
        element.remove();
      }
    },
    duration,
  );
}

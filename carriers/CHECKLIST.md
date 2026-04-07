# Exhaustive Analysis Checklist

Fallback checklist for unrecognized formats:

📁 LSB
🔥 Critical	Generic LSB Scan	Try LSB extraction on raw pixel data

📁 Strings
🔥 Critical	String Extraction	Extract printable strings from file

📁 Analysis
⚡ High	Magic Byte Scan	Look for embedded file signatures
📌 Medium	Entropy Analysis	Find high-entropy regions (possible encrypted data)
⚡ High	Polyglot File Detection	Check if file is valid as multiple formats
⚡ High	Binwalk-style Scan	Scan for embedded files at any offset
📎 Low	Repeated Pattern Detection	Find repeating byte sequences
📌 Medium	Compression Detection	Identify compressed regions (gzip, zlib, lzma)
⚡ High	StegSolve-style Analysis	Bit plane and color filter analysis

📁 Appended
🔥 Critical	Trailing/Appended Data	Data after expected file end

📁 Encoding
⚡ High	Base64 Detection	Look for Base64 encoded regions
📌 Medium	Hex String Detection	Look for hex-encoded data
📌 Medium	Unicode Steganography	Zero-width characters, homoglyphs, variation selectors
📌 Medium	Whitespace Steganography	Data in tabs/spaces/newlines patterns

📁 Encryption
📌 Medium	XOR Pattern Analysis	Detect single-byte XOR encryption
📌 Medium	Encryption Detection	High-entropy uniform distribution analysis

📁 Structure
📌 Medium	Null Region Analysis	Data hidden in null/zero padding areas

📁 Tools
📌 Medium	Steghide Signature	Look for Steghide tool markers
📌 Medium	OpenStego Signature	Look for OpenStego tool markers

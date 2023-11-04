console.info('contentScript is running')

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log(sender.tab ?
        "from a content script:" + sender.tab.url :
        "from the extension");
        
    if (request.type === 'COUNT') {
      console.log('contentScript has received a message from popup, and count is ', request?.count)
    }
  
    if (request.type === 'HTML') {
      console.log('contentScript has received a message from content, and html is ', request?.html)
    }

    else {
      console.log('contentScript has received a message and it is ', request)
    }
  })
  
  
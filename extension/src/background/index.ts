console.log('background is running')

chrome.runtime.onMessage.addListener((request) => {
  if (request.type === 'COUNT') {
    console.log('background has received a message from popup, and count is ', request?.count)
  }

  if (request.type === 'HTML') {
    console.log('background has received a message from content ')
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      // tabs[0] is the selected tab
      console.log('tabs', tabs)
      chrome.tabs.sendMessage(tabs[0].id! , {type: "HTML", html: "Hello from background!"});
    });
  }
})


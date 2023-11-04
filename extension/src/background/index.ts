console.log('background is running')

chrome.runtime.onMessage.addListener((request) => {
  if (request.type === 'COUNT') {
    console.log('background has received a message from popup, and count is ', request?.count)
  }

  if (request.type === 'HTML') {
    console.log('background has received a message from content, and html is ', request?.html)
  }
})


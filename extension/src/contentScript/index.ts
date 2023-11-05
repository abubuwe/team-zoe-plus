console.info('contentScript is running')

async function postData(url: string, data: any) {
  const response = await fetch(url, {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  });

  return response.json();
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log(sender.tab ?
        "from a content script:" + sender.tab.url :
        "from the extension");
        
    if (request.type === 'COUNT') {
      console.log('contentScript has received a message from popup, and count is ', request?.count)
    }
  
    if (request.type === 'HTML') {
      console.log('contentScript has received a message from content, and html is ', request?.html)
      const data = {"url": "http://www.google.com", "html_string": `<!DOCTYPE html>
      <html>
          <body>
              <h1>My First Heading</h1>
              <p>My first paragraph.</p>
          </body>
      </html>`};

      postData('http://127.0.0.1:5000', data)
      .then(data => {
          console.log(data); // API response
      });
    }

    else {
      console.log('contentScript has received a message and it is ', request)
    }
  })

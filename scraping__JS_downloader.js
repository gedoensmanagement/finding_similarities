// Load the page you want to save.
// On Alexander Street: Load the book. In the address field of your browser, delete "table-of-contents" and press Enter to reload the page.
// Scroll down to the very end of the page by pressing Ctrl-PAGE DOWN.
// Open the JavaScript console in your browser with Ctrl+Shift+i and select the "console" tab (if it is not already selected).
// Copy the code below.
// Paste the code in the console and press Enter. The function is now loaded and ready to use.
// Call the function by entering "downloader('<FILE.html>')" in the console replacing <FILE.html> by a filename of your choice.
// Press Enter. Confirm the download pop-up.
// Inspired by https://gist.github.com/danallison/3ec9d5314788b337b682 and
// https://stackoverflow.com/questions/11849562/how-to-save-the-output-of-a-console-logobject-to-a-file
function downloader(filename) {
    page = document.body.parentElement.innerHTML;
    var blob = new Blob([page], {type: 'text/html'});
    var a = document.createElement('a');
    a.download=filename;
    a.href = window.URL.createObjectURL(blob);
    a.dataset.downloadurl = ['text/html', a.download, a.href].join(':');
    var e = document.createEvent('MouseEvents');
    e.initMouseEvent('click', true, false, window, 0,0,0,0,0,false, false,false, false, 0, null);
    a.dispatchEvent(e);
}   

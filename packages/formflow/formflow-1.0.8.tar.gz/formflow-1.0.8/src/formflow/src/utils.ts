export function dedent(str: string) {
  // Remove leading newline
  str = str.replace(/^\n/, '');

  // Find the minimum indentation
  const match = str.match(/^[ \t]*(?=\S)/gm);
  const indent = match ? Math.min(...match.map(el => el.length)) : 0;

  // Create a regular expression to match leading whitespace
  const regex = new RegExp(`^[ \\t]{${indent}}`, 'gm');

  // Remove the leading whitespace
  return indent > 0 ? str.replace(regex, '') : str;
}

// This function expects a button where the previousElementSibling is a <pre>
// wrapping a <code> block and the nextElementSibling is an empty tooltip div.
//
export function copyToClipboard(button: any) {
    const codeBlock = button.previousElementSibling; // The code block before the button
    const text = codeBlock.textContent;

    navigator.clipboard.writeText(text).then(function() {
        // Show tooltip or change button text on success
        const tooltip = button.nextElementSibling;
        tooltip.textContent = "Copied!";
        tooltip.classList.add('show');
        setTimeout(() => {
            tooltip.classList.remove('show');
        }, 2000); // Hide the tooltip after 2 seconds
    }, function() {
        alert("There was an error copying the text");
    });
}

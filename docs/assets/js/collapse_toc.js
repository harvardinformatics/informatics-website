// This function expands/collapses 2nd-level TOC items
// Only top-level nav items with an active child link get the 'expanded' class
function expandActiveTOC() {
    // For each first-level nav item in the secondary navigation (the page ToC)
    document.querySelectorAll('.md-nav--secondary .md-nav__item').forEach(item => {
        // Find if this section has a child link marked as active (the current header in view)
        const active = item.querySelector('.md-nav__link--active');
        if (active) {
            // If so, add 'expanded' so CSS will show its children
            item.classList.add('expanded');
        } else {
            // Otherwise, collapse/hide its children
            item.classList.remove('expanded');
        }
    });
}

// Wait until the page is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Expand/collapse TOC for the initial state (on load)
    expandActiveTOC();

    // Every time the page scrolls (which may change the active header),
    // call the function to update the ToC expansion
    document.addEventListener('scroll', expandActiveTOC, true);

    // Additionally, listen for clicks on sidebar links — 
    // sometimes clicking doesn't cause a scroll but changes which header is active.
    // Set a short timeout so that any class changes from MkDocs Material's own JS run first.
    document.querySelectorAll('.md-nav--secondary .md-nav__link').forEach(link => {
        link.addEventListener('click', function () {
            setTimeout(expandActiveTOC, 50);
        });
    });
});
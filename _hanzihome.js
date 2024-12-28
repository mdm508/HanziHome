

// Process Hanzi characters and add rows with nested decomposition tables
function processHanziCharacters(hanziField, hz) {
    var container = $('#hanzihome'); // Fetch the element with id="hanzihome"

    Array.from(hanziField).forEach(char => {
        const data = hz[char]; // Fetch data for each Hanzi
        console.log(`Processing: ${char}`, data);

        // Handle missing data
        if (!data) {
            console.warn(`No data found for '${char}'`);
            return; // Skip this iteration
        }

        // Create main row for Hanzi details
        const row = $('<div>').addClass('hanzi-row'); // Add styling for the row

        // Hanzi Cell
        const hanziCell = $('<div>')
            .addClass('hanzi-cell hanzi') // Hanzi-specific style
            .text(data['character']);

        // Zhuyin Cell
        const zhuyinCell = $('<div>')
            .addClass('hanzi-cell zhuyin')
            .text(data['zhuyin'].join(", "));

        // Keyword Cell
        const keywordCell = $('<div>')
            .addClass('hanzi-cell keyword')
            .text(data['keyword']);

        // Create Decomposition Table
        const decompTable = createDecompositionTable(data['decomposition'], hz);

        // Append cells and table to row
        row.append(hanziCell, zhuyinCell, keywordCell, decompTable);

        // Add the completed row to the container
        container.append(row);
    });
}


function createDecompositionTable(decomp, hz) {
    const table = $('<div>').addClass('decomp-table'); // Create table with class
    Array.from(decomp).forEach(char => {
        const entry = hz[char] || { keyword: "" }; // Lookup each component

        // Create row for each component
        const row = $('<div>').addClass('decomp-row');

        // Hanzi Component
        const compCell = $('<div>')
            .addClass('decomp-cell')
            .text(char);

        // Keyword Component
        const keywordCell = $('<div>')
            .addClass('decomp-cell keyword')
            .text(entry['keyword']);

        // Append cells to row and row to table
        row.append(compCell, keywordCell);
        table.append(row);
    });

    return table;
}


// Inject CSS styles for layout
function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
/* Container for all rows */
#hanzihome {
    display: flex;
    flex-direction: column; /* Stack rows vertically */
    gap: 0.5rem;          /* 8px spacing between rows */
    padding: 0.5rem;      /* Outer padding */
}

/* Hanzi Row - Main container for each row */
.hanzi-row {
    display: flex;                     /* Horizontal layout for cells */
    align-items: center;               /* Vertically center align */
    justify-content: flex-start;       /* Align items to the start */
    padding: 0.0rem;                   /* Padding inside rows */
    border-top: 1px solid #ccc;
    border-bottom: 1px solid #ccc;     /* Row separators */
}

/* Hanzi Cells - Flexible row content */
.hanzi-cell {
    flex-grow: 1;                      /* Cells grow equally */
    text-align: left;                  /* Align text to the left */
    padding: 0.0rem;                  /* 4px padding */
}

/* Hanzi Character - Larger font size */
.hanzi-cell.hanzi {
    font-weight: bold;                 /* Bold font for emphasis */
    font-size: 4vw;                    /* Responsive font size based on viewport width */
}

/* Zhuyin and Keyword - Medium size */
.hanzi-cell.zhuyin,
.hanzi-cell.keyword {
    font-size: 3vw;                    /* Responsive size */
}

/* Decomposition Table */
.decomp-table {
    flex-basis: 20%;                   /* Fixed width for table */
    max-width: 20%;                    /* Prevent expansion */
    display: flex;
    flex-direction: column;            /* Vertical stacking */
    padding: 0.0rem;                  /* Padding inside table */
}

/* Decomposition Row */
.decomp-row {
    display: flex;                      /* Horizontal cells */
    width: 100%;                        /* Full width */
    justify-content: flex-start;        /* Align cells to the start */
    padding: 0.0rem 0;                /* 2px padding */
}

/* Decomposition Cells */
.decomp-cell {
    flex: 1;                            /* Equal size cells */
    padding: 0.0rem;                  /* 2px padding inside cells */
    font-size: 2.5vw;                   /* Responsive font size */
    text-align: left;                    /* Align text to the left */
}

/* Decomposition Keywords - Align Left */
.decomp-cell.keyword {
    text-align: left;                    /* Align keywords to start (left) */
}

/* Optional hover effect for clickable rows */
.hanzi-cell:hover, .decomp-cell:hover {
    background-color: #f0f0f0;
    cursor: pointer;
}
    `;
    document.head.appendChild(style);
}

//true means cloze is on the front side
function isFrontCloze(clozeText){
    return  clozeText === '[...]'
}

function getClozeValue() {
    const cloze = $('.cloze'); // Select the element with class 'cloze'
    const text = cloze.text().trim(); // Trim whitespace from text
    const dataCloze = cloze.attr('data-cloze'); // Get the 'data-cloze' attribute
    // Use ternary operator for concise conditional check
    const value = isFrontCloze(text) ? dataCloze : text;
    // Return filtered Chinese characters
    return filterChinese(value || ''); // Handle cases where value might be undefined
}

// Filter to keep only Chinese characters
function filterChinese(text) {
    return text.replace(/[^一-鿿]/g, '');
}

// Try to get the 'data' attribute directly from #hanzihome
function tryToGetData() {
    var hanziField = filterChinese($('#hanzihome').attr('data')); // Get 'data' attribute
    if (hanziField){
        return hanziField;
    }
    console.error("Missing 'data' attribute in #hanzihome.");
    console.error("Card must have a 'data' attribute in the #hanzihome div element.");
    return null;
}

function ifClozeExists() {
    return $('.cloze').length >= 1;
}

function getHanziField() {
    // Try cloze first

    if (ifClozeExists()){
        return getClozeValue();
    } else {
        var dataValue = tryToGetData();
        console.error("No valid Hanzi field found!");
        console.error("Card must have a valid cloze or 'data' attribute in the hanzihome div.");
    }
    return null; // Return null explicitly
}

// Fetch JSON and process Hanzi characters
fetch('_hanzihome.json')
    .then(response => response.text())       // Get raw text response
    .then(text => JSON.parse(text))          // Manually parse JSON
    .then(hz => {                            // Process parsed JSON
        injectStyles();                      // Inject CSS styles

        var hanziField = getHanziField();
        if (hanziField){
                processHanziCharacters(hanziField, hz);
        }

    })
    .catch(err => console.error("Something went wrong.", err));

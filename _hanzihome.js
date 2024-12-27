
// Helper function to create a row
function createRow(elements) {
    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.justifyContent = 'space-between';
    row.style.padding = '5px 0';

    elements.forEach(({ text, style = {} }) => {
        const div = document.createElement('div');
        div.textContent = text;

        // Apply optional styles
        Object.assign(div.style, style);
        row.appendChild(div);
    });

    return row;
}
function filterChinese(text) {
    return text.replace(/[^\u4E00-\u9FFF]/g, ''); // Keeps only Chinese characters
}

// Process each character in hanziField
function processHanziCharacters(hanziField, hz, container) {
    for (const char of hanziField) { // Loop through each character
        const data = hz[char]; // Fetch data for the character
        console.log(`Processing: ${char}`, data); // Debug each character

        // Handle missing data
        if (!data) {
            console.warn(`No data found for '${char}'`); // Warn instead of error
            continue; // Skip this character
        }

        // Create and append the row for the character
        container.appendChild(createRow([
            { text: data['character'], style: { fontWeight: 'bold' } },
            { text: data['zhuyin'].join(", ") },
            { text: data['keyword'] },
            { text: data['decomposition'] }
        ]));
    }
}

// Helper function to create a row
function createRow(elements) {
    const row = document.createElement('div');
    row.classList.add('hanzi-row'); // Add a class for consistent styling

    elements.forEach(({ text, style = {} }) => {
        const div = document.createElement('div');
        div.classList.add('hanzi-cell'); // Add cell styling
        div.textContent = text;

        // Apply optional styles
        Object.assign(div.style, style);
        row.appendChild(div);
    });

    return row;
}

// Inject CSS into the document head
function injectStyles() {
    const style = document.createElement('style');
    style.textContent = `
        #hanzihome {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .hanzi-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .hanzi-cell {
            flex: 1;
            text-align: center;
            padding: 5px;
        }

        .hanzi-cell:first-child {
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);
}


// Select container and extract data attribute
var container = document.getElementById('hanzihome');
var hanziField = filterChinese(container?.getAttribute('data'));
//Main Function
// Validate hanziField
if (!hanziField) {
    console.error("Missing 'data' attribute in template.");
    alert("missing data attribute in <div id=hanzihome data=?>")
}

fetch('_hanzihome.json')
    .then(response => response.text())       // Get raw text response
    .then(text => JSON.parse(text))          // Manually parse JSON
    .then(hz => {                            // Process parsed JSON
        console.log("Loaded JSON:", hz);     // Debug JSON data
			 injectStyles();
        processHanziCharacters(hanziField, hz, container);
    })
    .catch(err => console.error("Failed to load JSON:", err));



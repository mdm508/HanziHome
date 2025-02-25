# Hanzi Home
**Hanzi Home** is an Anki add-on designed to associate keywords with Chinese characters, inspired by the approach of *Remembering the Hanzi*. The goal is 
to help you manage information about Hanzi. This addon gives you a way too

1. look up information about chinese characters
2. display individual character breakdowns inside a table in your cards.

Information about characetrs stored in json file available on desktop and web.
Updates to keywords update this json file

## Demo

**Demo GIF**  
![Demo GIF](https://raw.githubusercontent.com/mdm508/HanziHome/master/demo/demo.gif)

**Table View**  
![Table View](https://raw.githubusercontent.com/mdm508/HanziHome/master/demo/table.png)

**Viewer Example**  
![Viewer Example](https://raw.githubusercontent.com/mdm508/HanziHome/master/demo/viewer.png)


## Table Setup

By embedding a simple `<div>` element onto your Anki card templates (for example, `<div id="hanzihome" data="{{Hanzi}}"></div>`), this add-on can generate a detailed table for each character. The table displays useful information such as:

- **Keyword** (mnemonic “keyword name” for the character)  
- **Reading** (currently uses Zhuyin, though Pinyin may be added in the future)  
- **Potential sub-components** (for prioritizing or referencing smaller parts of a character)

If you set it up correctly you will be able to use on Anki Mobile as well.
HanziViewer is limited to addon however.

### Inside the Card Template Editor add divs to Make Table

1. **Insert the div**: In the card template (Front/Back), add:
   ```html
   <div id="hanzihome" data="{{Hanzi}}"></div>
   ```
   or for cloze deletions:
   ```html
   <div id="hanzihome"></div>
   ```
2. **Configure**: Follow the detailed instructions in the add-on’s config file to set up the Hanzi data. You can specify keywords, component details, and more.

---

## Quick Search in your Hanzi Deck
**Hanzi Home** also makes it easier to search your existing Hanzi Deck (where you study
individual characters). 

When configured you will be abel so search for selected hanzi more quickly in
the browser. I wanted this because I often need to prioritize subcomponents that I have
forgotten.

![Demo GIF](https://raw.githubusercontent.com/mdm508/HanziHome/master/demo/search.gif)

### Quick Search Setup
Go to the config page for **Hanzi Home** and edit the config file to include

1. the deck you want to search
2. the field you want to limit the search to

Restart anki and try a search.

## Current Limitations

- **Traditional Focused**: Keywords and data focus on Traditional characters. You are probably still able to search and get information about
  simplified words, they will just lack keywords.
- **Zhuyin only**: The add-on displays phonetics in Zhuyin (Bopomofo). Pinyin support is not yet included.  
- **Features evolve on demand**

## Issues or Suggestions
Please open any issues or suggestions on [Github](https://github.com/mdm508/HanziHome)
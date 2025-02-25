# HanziHome Anki Add-on Configuration

## HanziViewer

- Documentation will be added later.

## Search your collection for a specific Hanzi

This configuration file is used for the HanziHome Anki add-on.

### Configuration Options

- **hanziFieldName**: Specifies the field name that contains the Hanzi characters.
- **deck**: Specifies the name of the deck to be used.

### Functionality

If you have a deck where you review individual characters, such as a Remember the Hanzi Deck, you may want to change the priority of certain characters (e.g., when struggling to remember a subcomponent of another character). This add-on allows you to quickly change the due date by configuring it to search for characters. You can right-click on a character and select "Search Hanzi in Hanzi Deck," which will auto-populate the browser with a search query to filter results to that specific character.

To enable this functionality, you need to edit the JSON configuration so the add-on knows which deck to search and which field contains the Hanzi characters.

### Example Configuration

```json
{
    "hanziFieldName": "hanzi",
    "deck": "remembering_traditional_hanzi"
}
```

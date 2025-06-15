/*
https://eldenring.fanapis.com/api/weapons?page=${currentPage.value}&limit=${itemsPerPage.value}
api call to get weapons returns a weapons object with a data property that contains an array of weapons
weapons are structured as follows:
{
  "attack": [
    "Phy": {
      "amount": "number",
      "name": "string",
    },
    "Mag": {
      "amount": "number",
      "name": "string",
    },
    "Fire": {
      "amount": "number",
      "name": "string",
    },
    "Lightning": {
      "amount": "number",
      "name": "string",
    },
    "Holy": {
      "amount": "number",
      "name": "string",
    },
    "Crit": {
      "amount": "number",
      "name": "string",
    }
  ],
  "category": "string",
  "defense": [
    "Phy": {
      "amount": "number",
      "name": "string",
    },
    "Mag": {
      "amount": "number",
      "name": "string",
    },
    "Fire": {
      "amount": "number",
      "name": "string",
    },
    "Lightning": {
      "amount": "number",
      "name": "string",
    },
    "Holy": {
      "amount": "number",
      "name": "string",
    },
    "Boost": {
      "amount": "number",
      "name": "string",
    }
  ],
  "description": "string",
  "id": "string",
  "image": "string",
  "name": "string",
  "requiredAttributes": [ // array of objects with name and amount
    {
      "name": "string",
      "amount": "number",
    }, ...
  ],
  "scalesWith": [
    {
      "name": "string",
      "scaling": "string",
      }, ...
  ],
  "weight": "number",
}
*/

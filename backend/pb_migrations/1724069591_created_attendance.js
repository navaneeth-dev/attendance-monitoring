/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "blix1jhjdsnhtyr",
    "created": "2024-08-19 12:13:11.690Z",
    "updated": "2024-08-19 12:13:11.690Z",
    "name": "attendance",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "vsuyqcgk",
        "name": "registerNo",
        "type": "number",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "noDecimal": false
        }
      },
      {
        "system": false,
        "id": "b16dcnbl",
        "name": "date",
        "type": "date",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": "",
          "max": ""
        }
      },
      {
        "system": false,
        "id": "mtxrsh8d",
        "name": "percentage",
        "type": "number",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "noDecimal": false
        }
      }
    ],
    "indexes": [],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("blix1jhjdsnhtyr");

  return dao.deleteCollection(collection);
})

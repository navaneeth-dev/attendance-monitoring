/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("d8qzvj5tqwfbinn")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "5mr91si7",
    "name": "studName",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("d8qzvj5tqwfbinn")

  // remove
  collection.schema.removeField("5mr91si7")

  return dao.saveCollection(collection)
})

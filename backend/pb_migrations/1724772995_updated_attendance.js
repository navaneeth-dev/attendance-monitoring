/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("blix1jhjdsnhtyr")

  // remove
  collection.schema.removeField("vsuyqcgk")

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("blix1jhjdsnhtyr")

  // add
  collection.schema.addField(new SchemaField({
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
  }))

  return dao.saveCollection(collection)
})

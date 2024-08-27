/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("blix1jhjdsnhtyr")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ntkja3qb",
    "name": "student",
    "type": "relation",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "collectionId": "d8qzvj5tqwfbinn",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": 1,
      "displayFields": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("blix1jhjdsnhtyr")

  // remove
  collection.schema.removeField("ntkja3qb")

  return dao.saveCollection(collection)
})

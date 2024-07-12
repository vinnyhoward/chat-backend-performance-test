const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();
const port = 3000;

app.use(express.json());

const uri = "mongodb://mongodb:27017/chatdb";
const client = new MongoClient(uri, { useUnifiedTopology: true });

app.post("/message", async (req, res) => {
  try {
    await client.connect();
    const collection = client.db("chatdb").collection("messages");
    const result = await collection.insertOne(req.body);
    res.status(201).json(result.ops[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  } finally {
    await client.close();
  }
});

app.listen(port, () => {
  console.log(`Node.js backend listening at http://localhost:${port}`);
});

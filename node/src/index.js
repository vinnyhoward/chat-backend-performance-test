const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();
const port = 3000;

app.use(express.json());

const uri = "mongodb://mongodb:27017/chatdb";
const client = new MongoClient(uri, { useUnifiedTopology: true });

let collection;

async function connectToMongo() {
  try {
    await client.connect();
    console.log("Connected to MongoDB");
    collection = client.db("chatdb").collection("messages");
  } catch (err) {
    console.error("Failed to connect to MongoDB", err);
    process.exit(1);
  }
}

app.post("/message", async (req, res) => {
  try {
    const result = await collection.insertOne(req.body);
    res.status(201).json({ ...req.body, _id: result.insertedId });
  } catch (err) {
    console.error("Error inserting message:", err);
    res.status(500).json({ error: err.message });
  }
});

connectToMongo().then(() => {
  app.listen(port, () => {
    console.log(`Node.js backend listening at http://localhost:${port}`);
  });
});

process.on("SIGINT", async () => {
  await client.close();
  console.log("MongoDB connection closed");
  process.exit(0);
});

import pg from "pg";
require("dotenv").config();

const db = new pg.Pool({ connectionString: process.env.DATABASE_URL });

db.connect((err, client, release) => {
  if (err) console.error("Connection failed:", err.message);
  else console.log("DB connected");
  release();
});

export { db };

import fs from "fs";
import { db } from "../src/db";
import path from "path";

const setup = async () => {
  const sql = fs.readFileSync(
    path.join(__dirname, "../queries/schema.sql"),
    "utf8",
  );
  await db.query(sql).then(() => console.log("Tables created"));
  process.exit(0);
};

setup().catch((err) => {
  console.error(err);
  process.exit(1);
});

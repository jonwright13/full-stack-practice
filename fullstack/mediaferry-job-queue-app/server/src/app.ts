import express, { Request, Response } from "express";
import multer from "multer";

import { db } from "./db";
import { PgJobsRepo } from "./adapters";
import { UserJobsService } from "./services";

const app = express();
const upload = multer({ dest: "uploads/" });

// To eliminate CORS errors
app.use(function (req, res, next) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept",
  );
  res.setHeader(
    "Access-Control-Allow-Methods",
    "POST, GET, PATCH, DELETE, OPTIONS",
  );
  next();
});
app.use(express.json());

app.get("/health", (req: Request, res: Response) => {
  res.json({ status: "ok" });
});

app.post(
  "/jobs",
  upload.single("file"),
  async (req: Request, res: Response) => {
    // TODO: insert job into DB
    const data = {
      file_name: req.file?.originalname ?? undefined,
      job_type: req.body.job_type,
      submitted_by: req.body.submitted_by,
    };

    if (!data.file_name || !data.job_type || !data.submitted_by) {
      res.status(400).json({ error: "Missing required fields" });
      return;
    }

    const repo = new PgJobsRepo();
    const service = new UserJobsService(repo);

    const row = await service.uploadJob(data);

    res.status(200).json(row);
  },
);

app.get("/jobs", async (req: Request, res: Response) => {
  const repo = new PgJobsRepo();
  const service = new UserJobsService(repo);

  const data = await service.getJobs();

  res.status(200).json(data);
});

export default app;

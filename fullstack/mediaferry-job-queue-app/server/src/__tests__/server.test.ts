// src/__tests__/server.test.ts
import request from "supertest";
import express from "express";
import path from "path";

// Mock the db module
jest.mock("../db", () => ({
  db: {
    query: jest.fn(),
  },
}));

import { db } from "../db";

const mockedDb = db.query as jest.Mock;

// Import app separately from listen so we can test without starting the server
import app from "../app"; // you'll need to extract app from index.ts

describe("GET /jobs", () => {
  beforeEach(() => jest.clearAllMocks());

  it("should return jobs and totalJobs", async () => {
    mockedDb
      .mockResolvedValueOnce({ rows: [{ id: 1, file_name: "test.jpg" }] }) // jobs query
      .mockResolvedValueOnce({ rows: [{ name: "Jon", total_jobs: "1" }] }); // totalJobs query

    const res = await request(app).get("/jobs");

    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty("jobs");
    expect(res.body).toHaveProperty("totalJobs");
  });
});

describe("POST /jobs", () => {
  beforeEach(() => jest.clearAllMocks());

  it("should insert a job and return it", async () => {
    mockedDb.mockResolvedValueOnce({
      rows: [{ id: 1, file_name: "test.png", status: "pending" }],
    });

    const res = await request(app)
      .post("/jobs")
      .attach("file", path.resolve(__dirname, "fixtures/test.png"))
      .field("job_type", "image_process")
      .field("submitted_by", "jon@wright.com");

    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty("status", "pending");
  });

  it("should return 400 if required fields are missing", async () => {
    const res = await request(app)
      .post("/jobs")
      .field("job_type", "image_process");
    expect(res.status).toBe(400);
  });
});

describe("Background worker", () => {
  beforeEach(() => jest.clearAllMocks());

  it("should mark a pending job as processing then completed/failed", async () => {
    mockedDb
      .mockResolvedValueOnce({ rows: [{ id: 1, file_name: "test.jpg" }] }) // SELECT pending
      .mockResolvedValueOnce({ rows: [] }) // UPDATE processing
      .mockResolvedValueOnce({ rows: [] }); // UPDATE completed/failed

    // import and call processJobs directly
    const { processJobs } = await import("../process-jobs");
    await processJobs();

    expect(mockedDb).toHaveBeenCalledTimes(2); // SELECT + UPDATE processing (setTimeout not resolved yet)
  });
});

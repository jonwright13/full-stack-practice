import { useEffect, useMemo, useState } from "react";
import { formatDistanceToNow } from "date-fns";

import "./App.css";

const ACCEPTED = ["image/png", "image/jpg", "image/jpeg", "text/csv"];
const OPTIONS = ["image_process", "csv_transform"] as const;
const URL = import.meta.env.VITE_API_URL;

interface Job {
  id: number;
  file_name: string;
  job_type: string;
  status: string;
  submitted_by: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  name: string;
}

interface TotalJob {
  name: string;
  total_jobs: string;
  has_failed_jobs: boolean;
  total_failed_jobs: string;
}

interface JobsData {
  jobs: Job[];
  totalJobs: TotalJob[];
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(true);
  const [jobs, setJobs] = useState<JobsData | null>(null);

  const fetchData = async (): Promise<void> => {
    try {
      console.log(`Fetching data`);
      const res = await fetch(`${URL}/jobs`);
      if (!res.ok) return;
      const data = (await res.json()) as JobsData;
      setJobs(data);
      setLoading(false);
    } catch (error: any) {
      console.log("Error fetching data", error);
    }
  };

  const uploadData = async (formData: FormData): Promise<void> => {
    try {
      const res = await fetch(`${URL}/jobs`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Error uploading data");
      // Refetch data after
      fetchData();
    } catch (error: any) {
      console.log("Error uploading", error);
      throw error;
    }
  };

  useEffect(() => {
    let timer: number | null = setInterval(fetchData, 3000);
    return () => clearInterval(timer);
  }, []);

  const parsedJobs = useMemo(() => {
    if (!jobs) return [];
    return jobs.jobs
      .sort((a, b) => a.id - b.id)
      .map((j) => {
        return {
          ...j,
          created_at: formatDistanceToNow(new Date(j.created_at), {
            addSuffix: true,
          }),
          updated_at: formatDistanceToNow(new Date(j.updated_at), {
            addSuffix: true,
          }),
        };
      });
  }, [jobs]);

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);

    const file = formData.get("upload") as File;
    const option = formData.get("option") as (typeof OPTIONS)[number];

    // Reject if no file detected
    if (!file || !file.name.length || file.size === 0) {
      alert("No file detected. Try again");
      return;
    }

    // Reject if no option selected
    if (!OPTIONS.includes(option)) {
      alert("Select an option first");
      return;
    }

    // Reject if file type is not in the allowed list
    if (!ACCEPTED.includes(file.type)) {
      alert(`Invalid filetype. File must be ${ACCEPTED}`);
      return;
    }

    // Reject if option is image process and the file is not an image type
    if (
      option === "image_process" &&
      !ACCEPTED.filter((i) => i !== "text/csv").includes(file.type)
    ) {
      alert(
        "Invalid file type for option image_process. File must be an image.",
      );
      return;
    }

    // Reject if option is csv transform and file is not a csv type
    if (option === "csv_transform" && file.type !== "text/csv") {
      alert("Invalid file type for option csv_transform. File must be a csv.");
      return;
    }

    formData.delete("upload");
    formData.append("file", file);
    formData.append("job_type", option);
    formData.append("submitted_by", "jon@wright.com");

    await uploadData(formData)
      .then(() => {
        form.reset();
        setSelectedFile(undefined);
      })
      .catch(() => alert("Error uploading file. Try again."));
  };

  return (
    <>
      <h1>MediaFerry Job Queue App</h1>
      <div>
        {/* File upload form */}
        <form className="upload-container" onSubmit={handleSubmit}>
          <div className="fields-container">
            <div className="file-input">
              <label htmlFor="file">Select a file</label>
              <input
                id="file"
                name="upload"
                type="file"
                accept=".png,.jpg,.jpeg,.csv"
                className="file"
                onChange={(e) => {
                  const fs = e.target.files;
                  if (!fs) return;
                  setSelectedFile(fs[0]);
                }}
              />
            </div>
            <select name="option">
              <option value="">Choose an option</option>
              <option value="image_process">Image Process</option>
              <option value="csv_transform">CSV Transform</option>
            </select>
          </div>
          <span className="filename">
            {selectedFile?.name ?? "No file selected..."}
          </span>
          <button type="submit">Upload</button>
        </form>

        {/* Table of jobs */}
        <div className="table-container">
          <h2>All Jobs</h2>

          {parsedJobs.length !== 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Job Type</th>
                  <th>Status</th>
                  <th>Submitted By</th>
                  <th>Created At</th>
                  <th>Updated At</th>
                </tr>
              </thead>
              <tbody>
                {parsedJobs.map((j) => (
                  <tr key={j.id}>
                    <td>{j.file_name}</td>
                    <td>{j.job_type}</td>
                    <td>{j.status}</td>
                    <td>{j.submitted_by}</td>
                    <td>{j.created_at}</td>
                    <td>{j.updated_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <>
              {loading ? (
                <div className="loader"></div>
              ) : (
                <span>No jobs yet. Create one.</span>
              )}
            </>
          )}
        </div>

        {/* Total Jobs */}
        <div className="table-container">
          <h2>Total Jobs</h2>
          {jobs && jobs.totalJobs.length ? (
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Total Jobs</th>
                  <th>Has Failed Jobs</th>
                  <th>Failed Jobs</th>
                </tr>
              </thead>
              <tbody>
                {jobs.totalJobs.map((j) => (
                  <tr key={j.name}>
                    <td>{j.name}</td>
                    <td>{j.total_jobs}</td>
                    <td>{String(j.has_failed_jobs)}</td>
                    <td>{j.total_failed_jobs}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <>
              {loading ? (
                <div className="loader"></div>
              ) : (
                <span>No jobs yet. Create one.</span>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}

export default App;

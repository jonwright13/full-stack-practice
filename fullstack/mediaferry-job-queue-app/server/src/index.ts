import app from "./app";
import { processJobs } from "./process-jobs";

setInterval(processJobs, 10000);

app.listen(3000, () => console.log("Running on port 3000"));

% List of open inputs
nrun = 1; % enter the number of runs here
jobfile = {'/scratch/wbic-beta/jt629/UKF_FS/99999/segment_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
spm('defaults', 'PET');
spm_jobman('run', jobs, inputs{:});

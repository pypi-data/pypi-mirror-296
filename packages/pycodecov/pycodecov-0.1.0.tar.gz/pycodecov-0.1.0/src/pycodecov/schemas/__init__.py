"""
Module to store common schema classes used by pycodecov.
"""

from .base_commit import BaseCommit
from .base_report_file import BaseReportFile
from .base_total import BaseTotal
from .branch import Branch
from .branch_detail import BranchDetail
from .commit import Commit
from .commit_comparison import CommitComparison
from .commit_coverage import CommitCoverage
from .commit_coverage_report import CommitCoverageReport
from .commit_coverage_total import CommitCoverageTotal
from .commit_detail import CommitDetail
from .commit_total import CommitTotal
from .component import Component
from .component_comparison import ComponentComparison
from .coverage_trend import CoverageTrend
from .diff_comparison import DiffComparison
from .file_change_summary_comparison import FileChangeSummaryComparison
from .file_comparison import FileComparison
from .file_name_comparison import FileNameComparison
from .file_stat_comparison import FileStatComparison
from .flag import Flag
from .flag_comparison import FlagComparison
from .git_author import GitAuthor
from .git_commit import GitCommit
from .line import Line
from .line_comparison import LineComparison
from .line_coverage_comparison import LineCoverageComparison
from .line_number_comparison import LineNumberComparison
from .owner import Owner
from .paginated_list import PaginatedList
from .pull import Pull
from .repo import Repo
from .repo_config import RepoConfig
from .report import Report
from .report_file import ReportFile
from .report_total import ReportTotal
from .total_comparison import TotalComparison
from .user import User

__all__ = [
    "BaseCommit",
    "BaseReportFile",
    "BaseTotal",
    "Branch",
    "BranchDetail",
    "Commit",
    "CommitComparison",
    "CommitCoverage",
    "CommitCoverageReport",
    "CommitCoverageTotal",
    "CommitDetail",
    "CommitTotal",
    "Component",
    "ComponentComparison",
    "CoverageTrend",
    "DiffComparison",
    "FileChangeSummaryComparison",
    "FileComparison",
    "FileNameComparison",
    "FileStatComparison",
    "Flag",
    "FlagComparison",
    "GitAuthor",
    "GitCommit",
    "Line",
    "LineComparison",
    "LineCoverageComparison",
    "LineNumberComparison",
    "Owner",
    "PaginatedList",
    "Pull",
    "Repo",
    "RepoConfig",
    "Report",
    "ReportFile",
    "ReportTotal",
    "TotalComparison",
    "User",
]

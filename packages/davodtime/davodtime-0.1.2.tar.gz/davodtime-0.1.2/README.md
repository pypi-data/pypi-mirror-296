# DavodTime CLI

A command line application (designed with the help of ChatGPT) designed to
produce timestamps in the format `MMddYYYY-HHmmss` across timezones.

```troff
.TH DAVODTIME 1 "August 2024" "Version 0.1.0" "User Commands"

.SH NAME
davodtime \- A command-line tool to display time in various formats.

.SH SYNOPSIS
.B davodtime
[\fButc\fR | \fIGMT\fR | \fITZ\fR | \fB-h\fR | \fB--help\fR]

.SH DESCRIPTION
.B davodtime
is a command-line utility that displays the current time in various time zones or formats.

.SH OPTIONS
.TP
.B -h, --help
Displays this help message and exits.

.TP
.B utc
Displays the current UTC (Coordinated Universal Time) in the format MMddYYYY-HHmmss.

.TP
.B TZ
Any standard timezone abbreviation (e.g., GMT, PST, EST) can be provided as an argument to display the current time in that timezone, in the format MMddYYYY-HHmmss.

.TP
If no arguments are provided, the local system time is displayed in the format MMddYYYY-HHmmss.

.SH EXAMPLES
.TP
.B davodtime
Displays the local system time.

.TP
.B davodtime utc
Displays the current time in UTC.

.TP
.B davodtime pst
Displays the current time in Pacific Standard Time.

.TP
.B davodtime -h
Displays the help message.

.SH AUTHOR
Your Name <your.email@example.com>

.SH LICENSE
This software is licensed under the MIT License.

.SH SEE ALSO
.B date(1)
```


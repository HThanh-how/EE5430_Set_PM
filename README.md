# EE5430 - Assignment 1: Transmission Lines

Three LaTeX solutions for Assignment 1 of **EE5430 - Microwave Engineering
and Systems**.

## Reports

| Student | ID | PDF | Source |
|---|---:|---|---|
| Nguyen Thai Thanh Binh | 2570175 | [PDF](pdf/EE5430_Assignment_1_Report_Nguyen_Thai_Thanh_Binh_2570175.pdf) | [TeX](src/EE5430_Assignment_1_Report_Nguyen_Thai_Thanh_Binh_2570175.tex) |
| Vu Tien Giang | 2570188 | [PDF](pdf/EE5430_Assignment_1_Report_Vu_Tien_Giang_2570188.pdf) | [TeX](src/EE5430_Assignment_1_Report_Vu_Tien_Giang_2570188.tex) |
| Pham Huy Thanh | 2570317 | [PDF](pdf/EE5430_Assignment_1_Report_Pham_Huy_Thanh_2570317.pdf) | [TeX](src/EE5430_Assignment_1_Report_Pham_Huy_Thanh_2570317.tex) |

## Layout

```text
.
|-- .github/workflows/latex.yml  # GitHub Actions validation
|-- assets/hcmut_logo.png        # Official HCMUT logo
|-- pdf/                          # Submission-ready PDFs
|-- src/                          # LaTeX sources and shared style
|-- build.ps1                     # Build all three reports
|-- .gitignore
`-- README.md
```

## Build

Install XeLaTeX (MiKTeX or TeX Live), then run from the repository root:

```powershell
./build.ps1
```

The script runs XeLaTeX twice per report, copies outputs to `pdf/`, and removes
auxiliary build files.

## Verified results

- Problem 1: `Z0 = 221.63 + j16.20 ohm`,
  `gamma = 0.04795 + j0.56349 1/m`, `lambda = 11.150 m`.
- Problem 2: `vp approximately 2.00e8 m/s`, `lambda approximately 0.400 m`.
- Problem 3: matched line length `3 lambda`; load voltage is in phase with the
  source.
- Problem 4: matched-load power `0.320 W`; an open circuit produces a standing
  wave with reflection coefficient `+1`.

Tagged releases attach the three final PDFs from `pdf/`.

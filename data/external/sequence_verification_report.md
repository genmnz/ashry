# Sequence verification against UniProtKB

Every accession was re-fetched from the UniProtKB REST API itself, not from a mirror. Identity is established by CRC64, the checksum UniProt publishes for each sequence, recomputed locally from the residues we hold. Length and mass are not sufficient: two variants of a protein, or one isoform's precursor and another's mature chain, can agree on both.

Accessions checked: 36

## Verdicts

- **ok**: 36

## Problems (0)

- none

## Sequence and entry versions

| accession | id | organism | len | seq ver | entry ver | last sequence update | CRC64 |
|---|---|---|---|---|---|---|---|
| P00698 | LYSC_CHICK | Gallus gallus | 147 | 1 | 253 | 1986-07-21 | `81E85743FF579468` |
| P00709 | LALBA_HUMAN | Homo sapiens | 142 | 1 | 215 | 1986-07-21 | `647F448733B06D65` |
| P00711 | LALBA_BOVIN | Bos taurus | 142 | 2 | 194 | 1989-07-01 | `810CDB1145901405` |
| P00794 | CHYM_BOVIN | Bos taurus | 381 | 3 | 193 | 2005-02-01 | `A4425013B4E2E56A` |
| P01005 | IOVO_CHICK | Gallus gallus | 210 | 1 | 174 | 1986-07-21 | `8BE9516B6D38ACF9` |
| P01012 | OVAL_CHICK | Gallus gallus | 386 | 2 | 211 | 2007-01-23 | `87179F028B20CEF2` |
| P01308 | INS_HUMAN | Homo sapiens | 110 | 1 | 285 | 1986-07-21 | `C2C3B23B85E520E5` |
| P01563 | IFNA2_HUMAN | Homo sapiens | 188 | 2 | 224 | 2022-05-25 | `9BAA221D2BFB421D` |
| P02189 | MYG_PIG | Sus scrofa | 154 | 2 | 137 | 2007-01-23 | `1CF92ACD400A76D0` |
| P02236 | LGB4_SOYBN | Glycine max | 145 | 2 | 142 | 2007-01-23 | `5A903EF234935F88` |
| P02461 | CO3A1_HUMAN | Homo sapiens | 1466 | 4 | 253 | 2007-01-23 | `B904B4E05E17D339` |
| P02662 | CASA1_BOVIN | Bos taurus | 214 | 2 | 179 | 1990-11-01 | `F066B5C8AE55828B` |
| P02663 | CASA2_BOVIN | Bos taurus | 222 | 2 | 160 | 1989-07-01 | `81E7408AF1C12F7C` |
| P02666 | CASB_BOVIN | Bos taurus | 224 | 2 | 196 | 1989-07-01 | `F0BBDD8148A238AE` |
| P02668 | CASK_BOVIN | Bos taurus | 190 | 1 | 176 | 1988-04-01 | `F12D8310C3B93EDA` |
| P02701 | AVID_CHICK | Gallus gallus | 152 | 3 | 193 | 2007-09-11 | `7795A458481AEC09` |
| P02754 | LACB_BOVIN | Bos taurus | 178 | 3 | 201 | 1991-08-01 | `225F10A78C63A6B2` |
| P02768 | ALBU_HUMAN | Homo sapiens | 609 | 2 | 299 | 1990-04-01 | `F88FF61DD242E818` |
| P02787 | TRFE_HUMAN | Homo sapiens | 698 | 5 | 272 | 2024-11-27 | `9A73B90D8C5671E9` |
| P02788 | TRFL_HUMAN | Homo sapiens | 710 | 6 | 271 | 2006-01-24 | `0489CABA6D13C098` |
| P02789 | TRFE_CHICK | Gallus gallus | 705 | 2 | 179 | 1996-02-01 | `864201A93146FA84` |
| P04141 | CSF2_HUMAN | Homo sapiens | 144 | 1 | 226 | 1986-11-01 | `75D1E50506BCA7A8` |
| P05231 | IL6_HUMAN | Homo sapiens | 212 | 1 | 260 | 1987-08-13 | `1F1ED1FE1B734079` |
| P09038 | FGF2_HUMAN | Homo sapiens | 288 | 3 | 264 | 2009-10-13 | `EAE98552A39D5E19` |
| P09919 | CSF3_HUMAN | Homo sapiens | 207 | 1 | 241 | 1989-07-01 | `421F635ECC776996` |
| P22301 | IL10_HUMAN | Homo sapiens | 178 | 1 | 233 | 1991-08-01 | `6825E9FA4337CDE4` |
| P24627 | TRFL_BOVIN | Bos taurus | 708 | 2 | 221 | 1993-10-01 | `C6FD7FC15D68E93F` |
| P31096 | OSTP_BOVIN | Bos taurus | 278 | 2 | 133 | 2006-06-27 | `8170204507864E87` |
| P40933 | IL15_HUMAN | Homo sapiens | 162 | 1 | 208 | 1995-02-01 | `0CE0520C1D8379E2` |
| P41365 | LIPB_MOEAN | Moesziomyces antarcticus | 342 | 1 | 105 | 1995-11-01 | `ACF1D83AED2E1A57` |
| P52754 | HYP1_TRIRF | Trichoderma reesei | 97 | 1 | 93 | 1996-10-01 | `F30907B331EC3175` |
| P56552 | DEF_PENBA | Pentadiplandra brazzeana | 54 | 1 | 93 | 1998-07-15 | `5BAB4D7215291252` |
| P59665 | DEF1_HUMAN | Homo sapiens | 94 | 1 | 198 | 2003-04-30 | `0E0F8E95737396FA` |
| P62694 | GUX1_TRIRF | Trichoderma reesei | 513 | 1 | 119 | 1986-07-21 | `9F5C0A8A854F2C12` |
| Q8IU54 | IFNL1_HUMAN | Homo sapiens | 200 | 1 | 167 | 2003-03-01 | `D4433B9462DCB4A1` |
| Q9UMD9 | COHA1_HUMAN | Homo sapiens | 1497 | 3 | 207 | 2007-05-01 | `E01027005F3AE843` |

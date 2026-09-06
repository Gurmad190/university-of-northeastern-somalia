# University of Northeastern Somalia website

Official static website source for the University of Northeastern Somalia (UNS), Garowe, Puntland, Somalia.

## Current production

- Website: https://uns-website-1.vercel.app
- Application form: https://form.jotform.com/262473510150043
- Pages: Home, About, Academics, Admissions, Learning Options, Research, Career Development, News & Events, and Contact

## Production build

Vercel runs:

```bash
python3 build_for_vercel.py
```

The build downloads the verified production source, routes every Apply action to the official Jotform, validates the result, and writes the deployable website to `dist/`.

To materialize the currently deployed public source into a local checkout instead, run:

```bash
python3 sync_from_vercel.py
```

## Content policy

Only verified UNS information should be published. Do not add unconfirmed accreditation, rankings, fees, deadlines, facilities, publications, vacancies, statistics, or partnerships. Use “Contact UNS for details” where information is unavailable.

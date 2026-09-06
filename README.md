# University of Northeastern Somalia website

This repository deploys the public UNS website and the **UNS Digital Portal** to the existing Vercel project.

## Digital Portal — Phase 1

The portal is available at `/portal/` and uses the existing UNS Digital Portal Supabase project.

- Roles: `main_admin`, `admin`, and `student`
- Authentication: institution-provisioned Supabase Auth accounts; public registration is disabled
- Records: Supabase-backed student profiles and news posts only
- Security: RLS policies permit students to read only their own profile; staff permissions are enforced in the database
- News: authorised staff can create, edit, publish/unpublish, and delete news

Excluded from this phase: fees, payments, grades, courses, lecturer management, and other advanced systems.

The tracked migration is at `supabase/migrations/20260906194500_phase1_portal.sql`.

## Deployment

Vercel runs `python3 build_for_vercel.py`. It needs `SUPABASE_URL` and `SUPABASE_PUBLISHABLE_KEY` configured in Vercel. `portal/config.js` is generated during the build and deliberately not committed. Never add a Supabase secret or service-role key to browser code or this repository.

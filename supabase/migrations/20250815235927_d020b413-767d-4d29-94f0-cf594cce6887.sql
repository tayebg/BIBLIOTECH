-- Remove the existing admin-only policies and replace with anonymous policies
-- First drop the existing admin-only policies for authors table
DROP POLICY IF EXISTS "Only admins can insert authors" ON public.authors;
DROP POLICY IF EXISTS "Only admins can update authors" ON public.authors;
DROP POLICY IF EXISTS "Only admins can delete authors" ON public.authors;

-- Drop the existing admin-only policies for books table
DROP POLICY IF EXISTS "Only admins can insert books" ON public.books;
DROP POLICY IF EXISTS "Only admins can update books" ON public.books;
DROP POLICY IF EXISTS "Only admins can delete books" ON public.books;
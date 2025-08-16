import { useState, useEffect } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

export interface Author {
  id: string;
  firstName: string;
  lastName: string;
  created_at?: string;
  updated_at?: string;
}

export const useAuthors = () => {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();

  const fetchAuthors = async () => {
    try {
      console.log('Fetching authors...');
      const { data, error } = await supabase
        .from('authors')
        .select('*')
        .order('last_name', { ascending: true });
      
      console.log('Fetch authors response:', { data, error });

      if (error) throw error;

      const mappedAuthors = data.map(author => ({
        id: author.id,
        firstName: author.first_name,
        lastName: author.last_name,
        created_at: author.created_at,
        updated_at: author.updated_at
      }));

      setAuthors(mappedAuthors);
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error fetching authors",
        description: error.message,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const addAuthor = async (firstName: string, lastName: string) => {
    try {
      console.log('Attempting to add author:', { firstName, lastName });
      const { data, error } = await supabase
        .from('authors')
        .insert([{ first_name: firstName, last_name: lastName }])
        .select()
        .single();
      
      console.log('Supabase response:', { data, error });

      if (error) throw error;

      const newAuthor = {
        id: data.id,
        firstName: data.first_name,
        lastName: data.last_name,
        created_at: data.created_at,
        updated_at: data.updated_at
      };

      setAuthors(prev => [...prev, newAuthor]);
      
      toast({
        title: "Author added",
        description: `${firstName} ${lastName} has been added successfully.`,
      });

      return { success: true };
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error adding author",
        description: error.message,
      });
      return { success: false, error: error.message };
    }
  };

  const updateAuthor = async (id: string, firstName: string, lastName: string) => {
    try {
      console.log('Attempting to update author:', { id, firstName, lastName });
      const { data, error } = await supabase
        .from('authors')
        .update({ first_name: firstName, last_name: lastName })
        .eq('id', id)
        .select()
        .single();

      if (error) throw error;

      const updatedAuthor = {
        id: data.id,
        firstName: data.first_name,
        lastName: data.last_name,
        created_at: data.created_at,
        updated_at: data.updated_at
      };

      setAuthors(prev => 
        prev.map(author => author.id === id ? updatedAuthor : author)
      );

      toast({
        title: "Author updated",
        description: `${firstName} ${lastName} has been updated successfully.`,
      });

      return { success: true };
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error updating author",
        description: error.message,
      });
      return { success: false, error: error.message };
    }
  };

  const deleteAuthor = async (id: string) => {
    try {
      console.log('Attempting to delete author:', { id });
      const { error } = await supabase
        .from('authors')
        .delete()
        .eq('id', id);

      if (error) throw error;

      setAuthors(prev => prev.filter(author => author.id !== id));
      
      toast({
        title: "Author deleted",
        description: "Author has been deleted successfully.",
      });

      return { success: true };
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error deleting author",
        description: error.message,
      });
      return { success: false, error: error.message };
    }
  };

  useEffect(() => {
    fetchAuthors();
  }, []);

  return {
    authors,
    isLoading,
    addAuthor,
    updateAuthor,
    deleteAuthor,
    refetch: fetchAuthors
  };
};
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Edit, Trash2, ChevronUp, ChevronDown } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuthors, Author } from '@/hooks/useAuthors';
import { useBooks } from '@/hooks/useBooks';

export const AuteursPage = () => {
  const { toast } = useToast();
  const { authors, isLoading: authorsLoading, addAuthor, updateAuthor, deleteAuthor } = useAuthors();
  const { books, isLoading: booksLoading } = useBooks();

  // Form state
  const [newAuthor, setNewAuthor] = useState({
    lastName: '',
    firstName: ''
  });

  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredAuthors, setFilteredAuthors] = useState<Author[]>([]);

  // Display state
  const [showBooks, setShowBooks] = useState(false);

  // Edit state
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({
    lastName: '',
    firstName: ''
  });
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  // Sorting state
  const [sortField, setSortField] = useState<'lastName' | 'firstName'>('lastName');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Update filtered authors when authors or search changes
  useEffect(() => {
    if (!searchQuery.trim()) {
      setFilteredAuthors(authors);
    } else {
      const filtered = authors.filter(author => 
        author.lastName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        author.firstName.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredAuthors(filtered);
    }
    setCurrentPage(1);
  }, [authors, searchQuery]);

  const handleAddAuthor = async () => {
    if (!newAuthor.lastName.trim() || !newAuthor.firstName.trim()) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive"
      });
      return;
    }

    const result = await addAuthor(newAuthor.firstName.trim(), newAuthor.lastName.trim());
    
    if (result.success) {
      setNewAuthor({
        lastName: '',
        firstName: ''
      });
    }
  };

  const handleDelete = async (id: string) => {
    await deleteAuthor(id);
  };

  const handleEdit = (author: Author) => {
    setEditingId(author.id);
    setEditForm({
      lastName: author.lastName,
      firstName: author.firstName
    });
    setIsEditModalOpen(true);
  };

  const handleSaveEdit = async () => {
    if (!editForm || !editingId) return;

    if (!editForm.lastName?.trim() || !editForm.firstName?.trim()) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive"
      });
      return;
    }

    const result = await updateAuthor(editingId, editForm.firstName.trim(), editForm.lastName.trim());
    
    if (result.success) {
      setEditingId(null);
      setEditForm({
        lastName: '',
        firstName: ''
      });
      setIsEditModalOpen(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditForm({
      lastName: '',
      firstName: ''
    });
    setIsEditModalOpen(false);
  };

  const getAuthorBooks = (author: Author) => {
    return books.filter(book => 
      book.authorId === author.id
    );
  };

  const handleToggleDisplay = () => {
    setShowBooks(!showBooks);
  };

  const handleSort = (field: 'lastName' | 'firstName') => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const sortedAuthors = [...filteredAuthors].sort((a, b) => {
    const aVal = a[sortField]?.toString().toLowerCase() || '';
    const bVal = b[sortField]?.toString().toLowerCase() || '';
    
    if (sortDirection === 'asc') {
      return aVal.localeCompare(bVal);
    } else {
      return bVal.localeCompare(aVal);
    }
  });

  const totalPages = Math.ceil(sortedAuthors.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedAuthors = sortedAuthors.slice(startIndex, endIndex);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  if (authorsLoading || booksLoading) {
    return (
      <div className="container mx-auto max-w-7xl flex items-center justify-center py-8">
        <div className="text-lg text-card-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto max-w-7xl space-y-4 sm:space-y-6">
      {/* Add Author Form */}
      <div className="bg-card rounded-xl p-4 sm:p-6 shadow-lg border border-white/10">
        <h2 className="text-lg sm:text-xl font-semibold text-card-foreground mb-4">Add Author</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-end">
          <div className="sm:col-span-1">
            <label className="text-sm font-medium text-card-foreground block mb-2">Last Name</label>
            <Input
              value={newAuthor.lastName}
              onChange={(e) => setNewAuthor({...newAuthor, lastName: e.target.value})}
              placeholder="Last Name"
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
          <div className="sm:col-span-1">
            <label className="text-sm font-medium text-card-foreground block mb-2">First Name</label>
            <Input
              value={newAuthor.firstName}
              onChange={(e) => setNewAuthor({...newAuthor, firstName: e.target.value})}
              placeholder="First Name"
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
          <div className="col-span-full sm:col-span-2">
            <Button variant="action" onClick={handleAddAuthor} className="w-full sm:w-auto min-h-[44px]">
              ADD
            </Button>
          </div>
        </div>
      </div>

      {/* Search Form */}
      <div className="bg-card rounded-xl p-4 sm:p-6 shadow-lg border border-white/10">
        <div className="flex flex-col sm:flex-row gap-4 items-end">
          <div className="flex-1 space-y-2">
            <label className="text-sm font-medium text-card-foreground">Search author</label>
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by last name or first name..."
              className="bg-input-bg border-0 text-input-foreground min-h-[44px]"
            />
          </div>
        </div>
      </div>

      {/* Display Authors with Books Button */}
      <div className="bg-card rounded-xl p-4 sm:p-6 shadow-lg border border-white/10">
        <Button variant="action" onClick={handleToggleDisplay} className="w-full sm:w-auto min-h-[44px]">
          {showBooks ? 'HIDE BOOKS' : 'SHOW BOOKS'}
        </Button>
      </div>

      {/* Authors Display - Table on desktop, Cards on mobile */}
      <div className="bg-card rounded-xl shadow-lg border border-white/10 overflow-hidden">
        {/* Desktop Table View */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-input-bg">
                <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[200px]">
                  <button 
                    onClick={() => handleSort('lastName')}
                    className="flex items-center gap-1 hover:text-primary transition-colors"
                  >
                    Full Name 
                    {sortField === 'lastName' && (
                      sortDirection === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
                    )}
                  </button>
                </th>
                {showBooks && (
                  <th className="px-6 py-4 text-left text-sm font-semibold text-input-foreground min-w-[250px]">Associated Books</th>
                )}
                <th className="px-6 py-4 text-center text-sm font-semibold text-input-foreground min-w-[120px]">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {paginatedAuthors.length > 0 ? (
                paginatedAuthors.map((author, index) => {
                  const authorBooks = getAuthorBooks(author);
                  return (
                    <tr key={author.id} className={index % 2 === 0 ? 'bg-card' : 'bg-input-bg/20'}>
                      <td className="px-6 py-4">
                        <span className="text-card-foreground font-medium">
                          {author.lastName}, {author.firstName}
                        </span>
                      </td>
                      
                      {showBooks && (
                        <td className="px-6 py-4">
                          <div className="max-w-[250px]">
                            {authorBooks.length > 0 ? (
                              <div className="space-y-1">
                                {authorBooks.map(book => (
                                  <div key={book.id} className="text-sm text-card-foreground/80 bg-secondary/20 rounded px-2 py-1">
                                    <span className="font-medium">{book.title}</span>
                                    <span className="text-xs text-card-foreground/60 block sm:inline sm:ml-2">
                                      ({book.year}) - ISBN: {book.isbn}
                                    </span>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <span className="text-sm text-card-foreground/60 italic">
                                No associated books
                              </span>
                            )}
                          </div>
                        </td>
                      )}
                      
                      <td className="px-6 py-4">
                        <div className="flex justify-center gap-2">
                          <Dialog open={isEditModalOpen && editingId === author.id} onOpenChange={setIsEditModalOpen}>
                            <DialogTrigger asChild>
                              <Button variant="icon" size="icon" onClick={() => handleEdit(author)} className="h-8 w-8">
                                <Edit className="h-4 w-4" />
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-md mx-4">
                              <DialogHeader>
                                <DialogTitle>Edit Author</DialogTitle>
                              </DialogHeader>
                              <div className="space-y-4">
                                <div className="space-y-2">
                                  <label className="text-sm font-medium">Last Name</label>
                                  <Input
                                    value={editForm.lastName || ''}
                                    onChange={(e) => setEditForm({...editForm, lastName: e.target.value})}
                                    placeholder="Last Name"
                                    className="min-h-[44px]"
                                  />
                                </div>
                                <div className="space-y-2">
                                  <label className="text-sm font-medium">First Name</label>
                                  <Input
                                    value={editForm.firstName || ''}
                                    onChange={(e) => setEditForm({...editForm, firstName: e.target.value})}
                                    placeholder="First Name"
                                    className="min-h-[44px]"
                                  />
                                </div>
                                <div className="flex flex-col sm:flex-row justify-end gap-2">
                                  <Button variant="outline" onClick={handleCancelEdit} className="w-full sm:w-auto min-h-[44px]">
                                    Cancel
                                  </Button>
                                  <Button variant="action" onClick={handleSaveEdit} className="w-full sm:w-auto min-h-[44px]">
                                    Save
                                  </Button>
                                </div>
                              </div>
                            </DialogContent>
                          </Dialog>
                          <Button variant="destructive" size="icon" onClick={() => handleDelete(author.id)} className="h-8 w-8">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={showBooks ? 3 : 2} className="px-6 py-8 text-center text-card-foreground/60">
                    {searchQuery ? 'No results found' : 'No authors available'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Mobile Card View */}
        <div className="md:hidden space-y-4 p-4">
          {paginatedAuthors.length > 0 ? (
            paginatedAuthors.map((author) => {
              const authorBooks = getAuthorBooks(author);
              return (
                <div key={author.id} className="bg-input-bg/20 rounded-lg p-4 space-y-3">
                  <div className="flex justify-between items-start">
                    <div className="space-y-2 flex-1">
                      <h3 className="text-lg font-semibold text-card-foreground">
                        {author.firstName} {author.lastName}
                      </h3>
                      {showBooks && (
                        <div className="space-y-2">
                          <p className="text-sm font-medium text-card-foreground/80">Associated Books:</p>
                          {authorBooks.length > 0 ? (
                            <div className="space-y-2">
                              {authorBooks.map(book => (
                                <div key={book.id} className="text-sm text-card-foreground/80 bg-secondary/20 rounded p-2">
                                  <span className="font-medium block">{book.title}</span>
                                  <span className="text-xs text-card-foreground/60">
                                    ({book.year}) - ISBN: {book.isbn}
                                  </span>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <span className="text-sm text-card-foreground/60 italic">
                              No associated books
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="flex gap-2 ml-4">
                      <Dialog open={isEditModalOpen && editingId === author.id} onOpenChange={setIsEditModalOpen}>
                        <DialogTrigger asChild>
                          <Button variant="icon" size="icon" onClick={() => handleEdit(author)} className="h-10 w-10 min-h-[44px]">
                            <Edit className="h-5 w-5" />
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="mx-4 max-w-sm">
                          <DialogHeader>
                            <DialogTitle>Edit Author</DialogTitle>
                          </DialogHeader>
                          <div className="space-y-4">
                            <div className="space-y-2">
                              <label className="text-sm font-medium">Last Name</label>
                              <Input
                                value={editForm.lastName || ''}
                                onChange={(e) => setEditForm({...editForm, lastName: e.target.value})}
                                placeholder="Last Name"
                                className="min-h-[44px]"
                              />
                            </div>
                            <div className="space-y-2">
                              <label className="text-sm font-medium">First Name</label>
                              <Input
                                value={editForm.firstName || ''}
                                onChange={(e) => setEditForm({...editForm, firstName: e.target.value})}
                                placeholder="First Name"
                                className="min-h-[44px]"
                              />
                            </div>
                            <div className="flex flex-col gap-2">
                              <Button variant="action" onClick={handleSaveEdit} className="w-full min-h-[44px]">
                                Save
                              </Button>
                              <Button variant="outline" onClick={handleCancelEdit} className="w-full min-h-[44px]">
                                Cancel
                              </Button>
                            </div>
                          </div>
                        </DialogContent>
                      </Dialog>
                      <Button variant="destructive" size="icon" onClick={() => handleDelete(author.id)} className="h-10 w-10 min-h-[44px]">
                        <Trash2 className="h-5 w-5" />
                      </Button>
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="text-center text-card-foreground/60 py-8">
              {searchQuery ? 'No results found' : 'No authors available'}
            </div>
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center gap-2 p-4 border-t border-white/10">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </Button>
            
            <div className="flex gap-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <Button
                  key={page}
                  variant={currentPage === page ? "action" : "outline"}
                  size="sm"
                  onClick={() => handlePageChange(page)}
                  className="min-w-[40px]"
                >
                  {page}
                </Button>
              ))}
            </div>
            
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};
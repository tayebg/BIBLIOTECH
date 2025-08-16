import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { User, BookOpen } from 'lucide-react';
import { LivresPage } from './LivresPage';
import { AuteursPage } from './AuteursPage';

type PageType = 'home' | 'livres' | 'auteurs';

export const BiblioTechLayout = () => {
  const [currentPage, setCurrentPage] = useState<PageType>('home');

  const handlePageChange = (page: PageType) => {
    setCurrentPage(page);
  };

  const handleQuit = () => {
    // Cancel any current actions and reset state
    setCurrentPage('home');
    // This will trigger a full reset of child components when they unmount/remount
  };


  return (
    <TooltipProvider>
      <div className="min-h-screen bg-background">
        {/* Fixed Top Navigation Bar */}
        <header className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-white/10">
          <div className="max-w-7xl mx-auto px-3 sm:px-6 py-2 sm:py-4">
            <div className="flex items-center justify-between gap-2 sm:gap-4">
              {/* Logo */}
              <div>
                <h1 className="text-lg sm:text-2xl font-bold text-foreground tracking-wide">
                  LIBRARY SYSTEM
                </h1>
                <p className="text-xs text-foreground/60">
                  Library Management System
                </p>
              </div>
              
              {/* Navigation Container */}
              <div className="flex items-center gap-1 sm:gap-4">
                {/* Navigation Buttons */}
                <div className="flex items-center gap-1 sm:gap-3 bg-white/10 rounded-lg p-1 sm:p-2 backdrop-blur-sm">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button 
                        variant={currentPage === 'auteurs' ? 'nav-active' : 'nav'}
                        onClick={() => handlePageChange('auteurs')}
                        className="p-2 sm:px-6 sm:py-2 text-sm font-medium min-h-[40px] sm:min-h-[44px]"
                      >
                        <User className="h-4 w-4 sm:hidden" />
                        <span className="hidden sm:inline">AUTHORS</span>
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Manage Authors</p>
                    </TooltipContent>
                  </Tooltip>
                  
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button 
                        variant={currentPage === 'livres' ? 'nav-active' : 'nav'}
                        onClick={() => handlePageChange('livres')}
                        className="p-2 sm:px-6 sm:py-2 text-sm font-medium min-h-[40px] sm:min-h-[44px]"
                      >
                        <BookOpen className="h-4 w-4 sm:hidden" />
                        <span className="hidden sm:inline">BOOKS</span>
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Manage Books</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
                
                {/* Action Buttons */}
                <div className="flex items-center gap-1 sm:gap-2">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button 
                        variant="exit"
                        onClick={handleQuit}
                        className="p-2 sm:px-4 sm:py-2 text-sm font-medium min-h-[40px] sm:min-h-[44px]"
                      >
                        <span className="hidden sm:inline">HOME</span>
                        <span className="sm:hidden">HOME</span>
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Back to home</p>
                    </TooltipContent>
                  </Tooltip>
                </div>
              </div>
            </div>
          </div>
        </header>

      {/* Main Content */}
      <main className="pt-32 sm:pt-24 min-h-screen px-4 sm:px-6">
        {currentPage === 'home' && (
          <div className="flex items-center justify-center min-h-[80vh] px-4">
            <div className="text-center max-w-2xl mx-auto">
              <h2 className="text-2xl sm:text-4xl lg:text-5xl font-bold text-foreground mb-4 sm:mb-6">
                Welcome to Library System
              </h2>
              <p className="text-base sm:text-xl text-foreground/80 mb-6 sm:mb-8">
                Modern Library Management System
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
                <Button 
                  variant="action" 
                  size="lg" 
                  onClick={() => handlePageChange('livres')}
                  className="w-full sm:w-auto"
                >
                  Manage Books
                </Button>
                <Button 
                  variant="action" 
                  size="lg" 
                  onClick={() => handlePageChange('auteurs')}
                  className="w-full sm:w-auto"
                >
                  Manage Authors
                </Button>
              </div>
            </div>
          </div>
        )}
        
        {currentPage === 'livres' && <LivresPage />}
        {currentPage === 'auteurs' && <AuteursPage />}
      </main>
      </div>
    </TooltipProvider>
  );
};
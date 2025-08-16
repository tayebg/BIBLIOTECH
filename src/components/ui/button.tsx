import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        // BiblioTech navigation buttons - transparent white/blue
        nav: "bg-white/20 text-foreground border border-white/30 hover:bg-action hover:text-action-foreground backdrop-blur-sm",
        "nav-active": "bg-action text-action-foreground shadow-lg",
        // BiblioTech input style
        input: "bg-input-bg text-input-foreground border-0 hover:bg-hover",
        // BiblioTech action buttons
        action: "bg-action text-action-foreground shadow hover:bg-accent-hover",
        // Exit button
        exit: "bg-secondary text-secondary-foreground hover:bg-hover",
        // Icon buttons
        icon: "bg-transparent hover:bg-hover text-card-foreground p-2 rounded-md",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        // Keep existing variants for compatibility
        outline: "border border-input-bg bg-card hover:bg-hover hover:text-input-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-hover",
        ghost: "hover:bg-hover hover:text-input-foreground",
        link: "text-action underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-6 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-12 rounded-lg px-8 text-base",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }

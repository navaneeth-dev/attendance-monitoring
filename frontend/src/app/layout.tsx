// app/layout.tsx
import React from "react";
import "./globals.css"; // Import global styles if any

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <html>
      <body>
        <main className="w-full">{children}</main>
        <footer></footer>
      </body>
    </html>
  );
};

export default Layout;

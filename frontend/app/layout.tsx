import type { Metadata } from "next";
import "leaflet/dist/leaflet.css";
import "./globals.css";
import { Footer, Nav } from "../components/Shell";

export const metadata: Metadata = { title: "SafeSpot | Community safety awareness", description: "Anonymous, non-emergency community safety awareness." };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="en"><body><Nav /><main className="container">{children}</main><Footer /></body></html>; }

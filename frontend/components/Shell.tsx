"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Shell.module.css";
const links = [["/", "Dashboard"], ["/report", "Report a concern"], ["/map", "Community map"], ["/tips", "Safety tips"], ["/admin", "Moderation"]] as const;
export function Nav() { const path = usePathname(); return <header className={styles.header}><div className={`container ${styles.nav}`}><Link href="/" className={styles.brand}>Safe<span>Spot</span></Link><nav aria-label="Main navigation">{links.map(([href,label]) => <Link key={href} href={href} className={path===href ? styles.active : ""}>{label}</Link>)}</nav></div></header>; }
export function Footer() { return <footer className={styles.footer}><div className="container"><strong>SafeSpot</strong><p>Community awareness, not emergency response. Share only approximate, non-identifying information.</p></div></footer>; }

import { EmergencyNotice } from "../../components/Notice";
import styles from "./tips.module.css";
const tips=[
 ["Road safety","Use well-lit routes where possible, obey crossings, and record road hazards with a broad landmark so others can make informed choices."],
 ["Personal safety","Trust your instincts, stay aware of your surroundings, and consider walking with someone or sharing a planned route with a trusted person when appropriate."],
 ["Report responsibly","Describe observable conditions and patterns, not assumptions about people. Keep reports anonymous and avoid names, contact details, private addresses, photos of people, or accusations."],
 ["When to contact emergency services","If there is immediate danger, a crime in progress, a medical emergency, or a threat to someone’s safety, contact local emergency services instead of using SafeSpot."],
];
export default function TipsPage(){return <><p className="eyebrow">Practical guidance</p><h1 className="page-heading">Safety tips for everyday awareness</h1><p className="page-intro">Small, thoughtful actions can help people navigate their community with more confidence.</p><EmergencyNotice/><div className={styles.grid}>{tips.map(([title,copy],i)=><article className="card" key={title}><span className={styles.number}>0{i+1}</span><h2>{title}</h2><p>{copy}</p></article>)}</div></>}

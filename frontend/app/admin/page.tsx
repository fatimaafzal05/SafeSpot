import { AdminPanel } from "../../components/AdminPanel";
export default function AdminPage(){return <><p className="eyebrow">Portfolio moderation</p><h1 className="page-heading">Moderate incoming reports</h1><p className="page-intro">Only reports you approve appear on the public dashboard and map. The password is checked by the backend and is never included in client code.</p><AdminPanel/></>}

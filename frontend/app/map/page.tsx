import CommunityMap from "../../components/MapLoader";
import { EmergencyNotice } from "../../components/Notice";
export default function MapPage(){return <><p className="eyebrow">Community context</p><h1 className="page-heading">Community safety map</h1><p className="page-intro">Only approved reports with voluntarily shared broad coordinates appear here. Pins are community awareness signals, not live incident alerts.</p><EmergencyNotice/><CommunityMap/></>}

import PathFinder from "geojson-path-finder";
import geojson from "./data/nodespatos.json";

const pathFinder = new PathFinder(geojson);

console.log(pathFinder);
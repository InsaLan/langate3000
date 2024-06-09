export interface Device {
  id: number;
  name: string;
  mac: string;
  whitelisted: boolean;
}

export interface UserDevice extends Device {
  user: number;
  ip: string;
  area: string;
}

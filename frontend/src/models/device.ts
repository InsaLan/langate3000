export interface Device {
  id: number;
  name: string;
  mac: string;
  enabled: boolean;
  whitelisted: boolean;
  bypass: boolean;
}

export interface UserDevice extends Device {
  user: string;
  ip: string;
}

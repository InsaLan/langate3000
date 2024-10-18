export interface EditableMark {
  name: string;
  value: number;
  priority: number;
}

export interface Mark extends EditableMark {
  devices: number;
  whitelisted: number;
}

export interface GameMark {
  [game: string]: number[];
}

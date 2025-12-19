export class BaseId {
  constructor(public readonly value: string) {
    if (!value) throw new Error("ID value cannot be empty");
  }
  toString() {
    return this.value;
  }
}

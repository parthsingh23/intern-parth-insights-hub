export function formatInr(amount: number): string {
  /*
    1. Use toFixed(2) to get a string with two decimal places.
    2. Split that string at ".".
    3. Separate the last three digits of the integer portion.
    4. Handle the remaining digits in groups of two.
    5. Reconstruct the formatted number with the decimal portion.
    */

  const formatted = amount.toFixed(2); // returns a string
  const parts = formatted.split('.');
  const integerPart = parts[0];
  const decimalPart = parts[1];
  const remaining = integerPart.slice(0, integerPart.length - 3);
  const lastThree = integerPart.slice(integerPart.length - 3);

  let grouped = '';
  let remainingDigits = remaining;

  while (remainingDigits.length > 2) {
    const lastTwo = remainingDigits.slice(-2);
    grouped = ',' + lastTwo + grouped;
    remainingDigits = remainingDigits.slice(0, -2);
  }

  grouped = remainingDigits + grouped;

  let result: string;

  if (grouped === '') {
    result = lastThree + '.' + decimalPart;
  } else {
    result = grouped + ',' + lastThree + '.' + decimalPart;
  }

  return result;
}

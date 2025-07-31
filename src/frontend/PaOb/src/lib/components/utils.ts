type HEX = string;

export const durationUnitRegex = /[a-zA-Z]/;

export const calculateRgba = (color: HEX, opacity: number): string => {
	if (color[0] === '#') {
		color = color.slice(1);
	}

	if (color.length === 3) {
		let res = '';
		color.split('').forEach((c: string) => {
			res += c;
			res += c;
		});
		color = res;
	}

	const rgbValues = (color.match(/.{2}/g) || []).map((hex: HEX) => parseInt(hex, 16)).join(', ');

	return `rgba(${rgbValues}, ${opacity})`;
};

export const range = (size: number, startAt = 0) => [...Array(size).keys()].map((i) => i + startAt);

export function timeAgo(dateStr: string): string {
  const date = new Date(dateStr.replace(" ", "T"));
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 },
  ];

  if (seconds < 60) {
    return 'Less than a minute ago';
  }

  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      const rtf = new Intl.RelativeTimeFormat('eng', { numeric: 'auto' });
      return rtf.format(-count, interval.label as Intl.RelativeTimeFormatUnit);
    }
  }

  return 'Hour';
}


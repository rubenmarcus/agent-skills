export function summarize(events) {
  const ids = [];
  for (const event of events) if (!ids.includes(event.userId)) ids.push(event.userId);
  return {
    totalEvents: events.length,
    participants: ids.map(userId => ({userId, events:events.filter(event => event.userId === userId).length}))
  };
}

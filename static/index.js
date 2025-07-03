exports = function(changeEvent) {
  const twilio = context.services.get("Twilio");
  const workers = context.services.get("mongodb-atlas").db("llr_db").collection("workers");
  
  if (changeEvent.operationType === "insert") {
    const phone = changeEvent.fullDocument.phone;
    twilio.send({
      to: phone,
      from: context.values.get("twilioNumber"),
      body: "Thanks for registering with LLR! Your account is now active."
    });
  }
};

package org.jeongkkili.bombom.member.exception;

public class ApproveReqNotFoundException extends RuntimeException {

	public ApproveReqNotFoundException() {
	}

	public ApproveReqNotFoundException(String message) {
		super(message);
	}

	public ApproveReqNotFoundException(String message, Throwable cause) {
		super(message, cause);
	}

	public ApproveReqNotFoundException(Throwable cause) {
		super(cause);
	}

	protected ApproveReqNotFoundException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}

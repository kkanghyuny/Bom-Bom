package org.jeongkkili.bombom.member.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.CONFLICT)
public class AlreadyExistIdException extends RuntimeException {

	public AlreadyExistIdException() {
	}

	public AlreadyExistIdException(String message) {
		super(message);
	}

	public AlreadyExistIdException(String message, Throwable cause) {
		super(message, cause);
	}

	public AlreadyExistIdException(Throwable cause) {
		super(cause);
	}

	protected AlreadyExistIdException(String message, Throwable cause, boolean enableSuppression,
		boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}
}

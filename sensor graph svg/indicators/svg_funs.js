
//=========================
// Вспомогательные функции
//=========================

// Функции из Интернета, немного доработанные

function polarToCartesian(centerX, centerY, radius, angleInDegrees) {

	var angleInRadians = (angleInDegrees-90) * Math.PI / 180.0;

	return {
		x: centerX + (radius * Math.cos(angleInRadians)),
		y: centerY + (radius * Math.sin(angleInRadians))
	};
}

function describeArc(x, y, radius, startAngle, endAngle){

	// По умолчанию угол отсчитывается от Pi/2 по часовой стрелке
	// Мы будем отсчитывать от положения Pi по часовой стрелке
	startAngle= startAngle<90 ? startAngle+270 : startAngle-90;
	endAngle= endAngle<90 ? endAngle+270 : endAngle-90;

	var start = polarToCartesian(x, y, radius, endAngle);
	var end = polarToCartesian(x, y, radius, startAngle);

	var arcSweep = endAngle - startAngle <= 180 ? 0 : 1;
	arcSweep = endAngle - startAngle < -0 ? 1 : arcSweep;
	arcSweep = endAngle - startAngle < -180 ? 0 : arcSweep;

	var d = [
		"M", start.x, start.y, 
		"A", radius, radius, 0, arcSweep, 0, end.x, end.y
	].join(" ");

	return d;       
}


